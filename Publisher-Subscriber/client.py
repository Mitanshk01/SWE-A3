import requests
from publishers.booking_request_publisher import BookingRequestPublisher
import json
from publishers.booking_response_publisher import BookingResponsePublisher
import uuid


def make_booking(venue_id, seats):
    request_Data = {
        "venueId": venue_id,
        "seats": seats
    }
    publisher = BookingRequestPublisher()
    request_id = str(uuid.uuid4())
    message = json.dumps(request_Data)
    publisher.publish(message)
    return request_id


def check_booking_status(request_id):
    publisher = BookingResponsePublisher()
    publisher.publish(request_id)
    print("Request sent to check booking status.")


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