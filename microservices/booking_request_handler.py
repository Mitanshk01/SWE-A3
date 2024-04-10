from flask import Flask, request, jsonify
import pika, json, uuid
import os

app = Flask(__name__)

def update_status(request_id, status):
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
    print("Checking status for request ID:", request_id)
    try:
        if not os.path.exists("request_status_db.json"):
            return "Unknown Request ID"  # File doesn't exist, implying no request has been made yet
        with open("request_status_db.json", "r") as file:
            data = json.load(file)
            print("Data:", data)
        return jsonify({"request_id": request_id, "status": data.get(request_id, "Unknown Request ID")})
    except json.JSONDecodeError:
        print("Looks like the file is empty or corrupted")
        return "Error reading status"  # In case the file is empty or corrupted

if __name__ == '__main__':
    app.run(debug=True, port=5001)