import pika

QUEUE_NAME = "crawl_queue"

def producer(seed_urls):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    for url in seed_urls:
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=url,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"[PRODUCER] Sent: {url}")

    connection.close()
    print("[PRODUCER] All URLs sent successfully")

if __name__ == "__main__":
    seed_urls = ["https://www.bing.com", "https://www.google.co.in"]
    producer(seed_urls)
