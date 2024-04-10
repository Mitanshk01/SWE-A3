from flask import Flask, request, jsonify
import pika, json, uuid
import os

app = Flask(__name__)

def update_status(request_id, status):
    """
    Update the status of a booking request.

    Parameters:
        request_id (str): The unique identifier of the booking request.
        status (str): The status to be updated for the booking request.

    Note:
        This function updates the status of a booking request in a JSON file.
        If the file doesn't exist, it creates a new file. If the file is empty
        or corrupted, it initializes an empty dictionary. It then updates the
        status for the given request ID and writes back the updated data to the file.
    """
    if not os.path.exists("request_status_db.json"):
        with open("request_status_db.json", "w") as file:
            json.dump({}, file)

    with open("request_status_db.json", "r+") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}

        data[request_id] = status
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

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

    update_status(request_id, "Pending")

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
        from a JSON file and returns it as a JSON response. If the file doesn't
        exist or if there's a JSON decoding error, appropriate error messages
        are returned.
    """
    try:
        if not os.path.exists("request_status_db.json"):
            return "Unknown Request ID"
        with open("request_status_db.json", "r") as file:
            data = json.load(file)
            print("Data:", data)

        return jsonify({"request_id": request_id, "status": data.get(request_id, "Unknown Request ID")})

    except json.JSONDecodeError:
        return "Error reading status"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
