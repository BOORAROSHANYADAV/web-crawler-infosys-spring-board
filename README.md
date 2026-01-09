🕷️ Distributed Web Crawler using RabbitMQ
📌 Project Overview

This project implements a Distributed Web Crawler and Indexer using Python and RabbitMQ. It follows a Producer–Worker–Indexer architecture to enable scalable, parallel, and reliable web crawling. The system can crawl multiple web pages simultaneously and build an inverted index using TF-IDF.

🧩 System Components
🔹 Producer

Sends initial seed URLs to the RabbitMQ queue.

Acts as the starting point of the crawling process.

🔹 Worker

Multiple workers run in parallel.

Consume URLs from the queue.

Fetch web pages and save HTML files.

Extract new links and push them back to the queue.

Ensures load balancing and scalability.

🔹 Indexer

Reads saved HTML pages.

Cleans and tokenizes text.

Builds an inverted index using TF-IDF.

Stores index data in JSON files.

🔹 RabbitMQ

Acts as a message broker.

Manages communication between Producer and Workers.

Ensures durability, reliability, and fault tolerance.

🏗️ Architecture Diagram (Logical)
Producer → RabbitMQ Queue → Workers → Saved HTML Pages → Indexer
                 ↑                 ↓
              New URLs ← Link Extraction

⚙️ Technologies Used

Python

RabbitMQ

Pika

Requests

Multiprocessing

▶️ How to Run the Project
1️⃣ Start RabbitMQ Server

Make sure RabbitMQ is running on your system.

2️⃣ Run Producer
python producer.py

3️⃣ Run Worker (Multiple Workers Supported)
python worker.py

4️⃣ Run Indexer
python indexer.py

📂 Project Structure
web-crawler/
├── producer.py
├── worker.py
├── indexer.py
├── saved_pages/
├── inverted_index.json
└── idf.json

✅ Key Features

Distributed crawling using RabbitMQ

Parallel processing with multiple workers

Durable queues and persistent messages

Automatic link extraction and re-queuing

TF-IDF based inverted index

Scalable and fault-tolerant design

🎯 Use Cases

Search engine prototype

Distributed data collection

Information retrieval systems

Academic and learning projects

📌 Conclusion

This project demonstrates how message queues like RabbitMQ can be used to design scalable distributed systems. By separating concerns into Producer, Worker, and Indexer components, the system achieves efficiency, reliability, and extensibility.

👤 Author

Roshan Yadav
