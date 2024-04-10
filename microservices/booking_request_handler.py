from flask import Flask, request, jsonify
import pika, json, uuid
import os
import sqlite3
from utilities import start_processing_request, get_status_from_db

app = Flask(__name__)

@app.route('/book', methods=['POST'])
def book():
    """
    Endpoint to book a service.

    Note:
        This endpoint receives a booking request, generates a unique request ID,
        updates the status as 'Pending' using the update_status() function,
        publishes the booking request message to a RabbitMQ server, and returns
        a response with status 202 (Accepted).
    """
    data = request.json
    request_id = str(uuid.uuid4())
    data['request_id'] = request_id

    start_processing_request(data)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
    channel.basic_publish(exchange='bookingExchange',
                          routing_key='booking_request',
                          body=json.dumps(data))
    connection.close()

    return jsonify({"status": "Pending", "message": "Booking request received", "request_id": request_id}), 202

@app.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    """
    Endpoint to check the status of a booking request.

    Parameters:
        request_id (str): The unique identifier of the booking request.

    Returns:
        str: A JSON response containing the status of the booking request.

    Note:
        This endpoint retrieves the status of the specified booking request
        from an SQLite database and returns it as a JSON response.
    """
    status = get_status_from_db(request_id)
    return jsonify({"request_id": request_id, "status": status})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
