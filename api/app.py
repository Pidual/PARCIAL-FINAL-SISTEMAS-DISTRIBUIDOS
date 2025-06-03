from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import pika
import json
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic authentication credentials
USER = "admin"
PASSWORD = "password"

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

@auth.verify_password
def verify_password(username, password):
    if username == USER and password == PASSWORD:
        return username
    return None

@app.route('/message', methods=['POST'])
@auth.login_required
def send_message():
    # Check if request has JSON data
    if not request.is_json:
        return jsonify({"error": "Request must contain JSON data"}), 400
    
    # Get JSON data from request
    message_data = request.get_json()
    
    try:
        # Connect to RabbitMQ
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        channel = connection.channel()
        
        # Declare the queue (creates it if it doesn't exist)
        channel.queue_declare(queue='messages', durable=True)
        
        # Publish message to the queue
        channel.basic_publish(
            exchange='',
            routing_key='messages',
            body=json.dumps(message_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        # Close the connection
        connection.close()
        
        return jsonify({"status": "Message sent successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Failed to send message: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker healthcheck"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)