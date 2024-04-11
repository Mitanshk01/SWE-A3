import pika
import json 

from utilities import start_processing_request, update_request_status,  get_venue_occupancy, update_venue_occupancy

class BookingRequestSubscriber:
    def __init__(self, exchange_name, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue_name)
        self.channel.basic_qos(prefetch_count=1)

    def process_booking(self, body):
        booking_data = json.loads(body)
        start_processing_request(booking_data)
        print(f"Processed booking request: {booking_data}")
        return booking_data 
    
    def update_booking_status(self, booking_data):
        request_id = booking_data['request_id']
        update_request_status(request_id,booking_data['status'])

    def seats_can_be_booked(self, venue_id, seats):
        venue_occupancy = get_venue_occupancy(venue_id)
        if venue_occupancy:
            max_occupancy = int(venue_occupancy[0])
            current_occupancy = int(venue_occupancy[1])
            if current_occupancy + int(seats) <= max_occupancy:
                return True
        return False
    
    def send_status_update(self, request_id, status):
        # publish the status on the booking_response_exchange
        self.channel.basic_publish(exchange='booking_response_exchange',
                        routing_key='',
                        body=json.dumps({"request_id": request_id, "status": status}))
        
        print(f" [x] Sent status update: {status}")

    def callback(self, ch, method, properties, body):
        print(" [x] Received message:", json.loads(body))
        self.process_booking(body)
        # ch.basic_publish(exchange='booking_response_exchange',
        #                 routing_key='booking_confirmation',
        #                 body=json.dumps(json.loads(body)))
        print(" [x] Sent booking confirmation")

        body = json.loads(body)
        request_id = body['request_id']
        venue_id = body['venueId']
        seats = body['seats']
        if self.seats_can_be_booked(venue_id, seats):
            update_venue_occupancy(venue_id, seats)
            body['status'] = 'Confirmed'
            self.update_booking_status(body)
            print(f"Booking confirmed: {body}")
            self.send_status_update(request_id, "Confirmed")
        else:
            body['status'] = 'Denied'
            self.update_booking_status(body)
            print(f"Booking denied: {body}")
            self.send_status_update(request_id, "Denied")

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()



# config = { 'host': 'localhost', 'port': 5672, 'exchange' : 'bookingRequestExchange'}
# if len(sys.argv) < 2:
#    print('Usage: ' + __file__ + ' <QueueName> <BindingKey>')
#    sys.exit()
# else:
#    queueName = sys.argv[1]
#    #key in the form exchange.*
#    key = sys.argv[2]
#    subscriber = Subscriber(queueName, key, config)
#    subscriber.setup()