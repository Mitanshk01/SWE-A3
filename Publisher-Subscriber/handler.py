from subscribers.booking_request_subscriber import BookingRequestSubscriber

class Handler:
    def __init__(self):
        self.booking_request_subscriber = BookingRequestSubscriber('booking_request_exchange', 'booking_request_queue')
    
    def start_consuming(self):
        self.booking_request_subscriber.start_consuming()


handler = Handler()
print("[Handler] Welcome to the Handler (Booking Request Subscriber)")
handler.start_consuming()
