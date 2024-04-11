from flask import Flask, request, jsonify
import pika, json, uuid

app = Flask(__name__)

@app.route('/book', methods=['POST'])
def book():
    """
    Endpoint to book a service.

    Note:
        This endpoint receives a booking request, generates a unique request ID,
        publishes the booking request message to a RabbitMQ server, and returns
        a response with status 202 (Accepted).
    """
    data = request.json
    request_id = str(uuid.uuid4())
    data['request_id'] = request_id

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='bookingExchange', exchange_type='direct')
    channel.basic_publish(exchange='bookingExchange',
                          routing_key='booking_request',
                          body=json.dumps(data))
    connection.close()

    return jsonify({"status": "Pending", "message": "Booking request received", "request_id": request_id}), 202

def send_status_check_request(request_id):
    """
    Send a status check request to the processor.py script.

    Parameters:
        request_id (str): The unique identifier of the booking request.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='status_exchange', exchange_type='direct')
    channel.basic_publish(exchange='status_exchange',
                          routing_key='status_check_request',
                          body=json.dumps({"request_id": request_id}))
    connection.close()

def get_status_from_processor(request_id):
    """
    Get the status of a booking request from the processor.py script.

    Parameters:
        request_id (str): The unique identifier of the booking request.

    Returns:
        str: The status of the booking request.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='status_response_queue')
    method_frame, header_frame, body = channel.basic_get(queue='status_response_queue', auto_ack=True)
    if body:
        response_data = json.loads(body)
        if response_data.get('request_id') == request_id:
            return response_data.get('status')
    return "Unknown Request ID"

@app.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    """
    Endpoint to check the status of a booking request.

    Parameters:
        request_id (str): The unique identifier of the booking request.

    Returns:
        str: A JSON response containing the status of the booking request.
    """
    send_status_check_request(request_id)
    status = get_status_from_processor(request_id)
    return jsonify({"request_id": request_id, "status": status})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
