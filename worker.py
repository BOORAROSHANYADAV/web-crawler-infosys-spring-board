import pika
import requests
import re
import os
import time
from multiprocessing import Process, Queue, Value

QUEUE_NAME = "crawl_queue"
SAVE_DIR = "saved_pages"
NUM_WORKERS = 3
MAX_TOTAL_PAGES = 20
MAX_PAGES_PER_WORKER = 10

def fetch_page(url, retries=3):
    for _ in range(retries):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException:
            pass
    return None

def save_page(worker_id, page_id, html):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = f"{SAVE_DIR}/worker{worker_id}_page{page_id}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SAVED] {path}")

def extract_links(html):
    return re.findall(r'href=["\'](http[s]?://[^"\']+)["\']', html)

def worker(worker_id, stats_queue, total_pages_crawled):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    visited = set()
    page_id = 1
    pages_crawled = 0

    def callback(ch, method, properties, body):
        nonlocal page_id, pages_crawled
        url = body.decode()

        with total_pages_crawled.get_lock():
            if total_pages_crawled.value >= MAX_TOTAL_PAGES:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                ch.stop_consuming()
                return

        if url in visited or page_id > MAX_PAGES_PER_WORKER:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f"[Worker-{worker_id}] Crawling: {url}")
        html = fetch_page(url)

        if not html:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        save_page(worker_id, page_id, html)
        pages_crawled += 1

        with total_pages_crawled.get_lock():
            total_pages_crawled.value += 1

        for link in extract_links(html):
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=link,
                properties=pika.BasicProperties(delivery_mode=2)
            )

        visited.add(url)
        page_id += 1
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

    stats_queue.put((worker_id, pages_crawled))

if __name__ == "__main__":
    start_time = time.time()
    total_pages_crawled = Value('i', 0)
    stats_queue = Queue()
    workers = []

    for i in range(NUM_WORKERS):
        p = Process(target=worker, args=(i+1, stats_queue, total_pages_crawled))
        p.start()
        workers.append(p)

    for p in workers:
        p.join()

    while not stats_queue.empty():
        wid, pages = stats_queue.get()
        print(f"Worker-{wid} crawled {pages} pages")

    print(f"Time taken: {time.time() - start_time:.2f} seconds")
