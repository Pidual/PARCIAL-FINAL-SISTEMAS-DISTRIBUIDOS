import pika
import json
import os
import time
from datetime import datetime

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

# Directory for persisting messages
DATA_DIR = "/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Health file for Docker healthcheck
HEALTH_FILE = "/app/health"

def callback(ch, method, properties, body):
    """Process messages from the queue"""
    try:
        # Parse the message JSON
        message = json.loads(body)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log message to console
        print(f"[{timestamp}] Received message: {message}")
        
        # Write message to persistent file
        with open(f"{DATA_DIR}/messages.log", "a") as f:
            f.write(f"[{timestamp}] {json.dumps(message)}\n")
        
        # Acknowledge the message (confirm it's been processed)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        # Update health file timestamp
        with open(HEALTH_FILE, "w") as f:
            f.write(timestamp)
            
    except Exception as e:
        print(f"Error processing message: {e}")
        # Negative acknowledgment, requeue the message
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    # Wait for RabbitMQ to be available
    connected = False
    while not connected:
        try:
            # Establish connection to RabbitMQ
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            connected = True
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    
    # Create channel
    channel = connection.channel()
    
    # Declare the queue (must match the one used by the producer)
    channel.queue_declare(queue='messages', durable=True)
    
    # Set quality of service - only process one message at a time
    channel.basic_qos(prefetch_count=1)
    
    # Set up consumer
    channel.basic_consume(queue='messages', on_message_callback=callback)
    
    # Initialize health file
    with open(HEALTH_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print("Worker started. Waiting for messages...")
    
    # Start consuming
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Worker stopped")