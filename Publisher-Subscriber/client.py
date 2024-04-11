from publishers.booking_request_publisher import BookingRequestPublisher
from subscribers.booking_request_subscriber import BookingRequestSubscriber
from publishers.booking_response_publisher import BookingResponsePublisher
from subscribers.booking_response_subscriber import BookingResponseSubscriber
import json
import uuid

# Define exchange names
booking_request_exchange = 'booking_request_exchange'
booking_response_exchange = 'booking_response_exchange'

# Define queue names
booking_request_queue = 'booking_request_queue'
booking_response_queue = 'booking_response_queue'

# Create publishers and subscribers
booking_request_publisher = BookingRequestPublisher(booking_request_exchange)
booking_response_publisher = BookingResponsePublisher(booking_response_exchange)

booking_request_subscriber = BookingRequestSubscriber(booking_request_exchange, booking_request_queue)
booking_response_subscriber = BookingResponseSubscriber(booking_response_exchange, booking_response_queue)


def make_booking(venue_id, seats):
    request_data = {"request_id": str(uuid.uuid4()), 
                    "venueId": venue_id, "seats": seats}
    booking_request_publisher.publish_message(request_data)

    return request_data["request_id"]

def check_booking_status(request_id):
    booking_response_publisher.publish_message({"request_id": request_id})
    return "TODO : Figure out how to get status from booking_response_subscriber"
    # return booking_response_subscriber.get_status(request_id)

if __name__ == "__main__":
    print("Welcome to the Booking Client")
    while True:
        action = input("Choose action - [1] Make Booking, [2] Check Status: ").strip()
        
        # Making a booking
        if action == "1":
            venue_id = input("Enter venue ID: ")
            seats = input("Enter number of seats: ")
            request_id = make_booking(venue_id, seats)

            if request_id:
                print(f"Booking request submitted. Request ID: {request_id}")
            else:
                print("Failed to make booking request.")
        
        # Checking booking status
        elif action == "2":
            request_id = input("Enter request ID to check status: ")
            status = check_booking_status(request_id)
            print(f"Booking Status for {request_id}: {status}")

        else:
            print("Invalid action selected.")