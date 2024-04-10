import requests

def make_booking(venue_id, seats):
    response = requests.post("http://localhost:5001/book", json={"venueId": venue_id, "seats": seats})
    if response.status_code == 202:
        return response.json()["request_id"]
    else:
        return None

def check_booking_status(request_id):
    response = requests.get(f"http://localhost:5001/status/{request_id}")
    if response.status_code == 200:
        return response.json()["status"]
    else:
        return "Error checking status"

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