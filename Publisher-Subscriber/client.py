from publishers.booking_request_publisher import BookingRequestPublisher
from publishers.booking_response_publisher import BookingResponsePublisher
from subscribers.booking_response_subscriber import BookingResponseSubscriber
import uuid


class Client:
    def __init__(self):
        self.booking_request_publisher = BookingRequestPublisher('booking_request_exchange')
        self.booking_response_publisher = BookingResponsePublisher('booking_response_exchange')
        self.booking_response_subscriber = BookingResponseSubscriber('booking_response_exchange', 'booking_response_queue')

    def make_booking(self, venue_id, seats):
        request_data = {"request_id": str(uuid.uuid4()), 
                        "venueId": venue_id, "seats": seats}
        self.booking_request_publisher.publish_message(request_data)

        return request_data["request_id"]

    def check_booking_status(self, request_id):
        self.booking_response_publisher.publish_message({"request_id": request_id})
        #TO DO:  return booking_response_subscriber.get_status(request_id)

    def print_booking_status(self, status):
        print(f"[CLient] Booking Status: {status}")

    def start_consuming(self):
        self.booking_response_subscriber.start_consuming()

    def close_connection(self):
        self.booking_response_subscriber.close_connection()

client = Client()

if __name__ == "__main__":
    print("[Client] Welcome to the Booking Client")
    while True:
        action = input("[Client] Choose action - [1] Make Booking, [2] Check Status: ").strip()
        
        # Making a booking
        if action == "1":
            venue_id = input("[Client] Enter venue ID: ")
            seats = input("[Client] Enter number of seats: ")
            request_id = client.make_booking(venue_id, seats)

            if request_id:
                print(f"[Client] Booking request submitted. Request ID: {request_id}")
            else:
                print("[Client] Failed to make booking request.")
        
        # Checking booking status
        elif action == "2":
            request_id = input("[Client] Enter request ID to check status: ")
            client.check_booking_status(request_id)
            # print(f"[Client] Booking Status for {request_id}: {status}")
        else:
            print("[Client] Invalid action selected.")