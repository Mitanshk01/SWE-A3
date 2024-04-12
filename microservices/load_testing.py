from locust import User, task, between, events
import uuid
from client import *
import random
import time

class BookingUser(User):
    wait_time = between(1, 5)
    request_ids = []

    def on_start(self):
        return

    @task
    def make_booking(self):
        start_time = time.time()
        venue_id = random.randint(1, 5)
        seats = random.randint(1, 50)
        request_id = make_booking(venue_id, seats)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        events.request.fire(request_type="make_booking", name="make_booking", response_time=response_time, response_length=0)
        if request_id:
            print(f"[Locust] Booking request submitted. Request ID: {request_id}")
            self.request_ids.append(request_id)
        else:
            print("[Locust] Failed to make booking request.")

    @task
    def check_booking_status(self):
        if self.request_ids:
            request_id = self.request_ids.pop(0)
            start_time = time.time()
            check_booking_status(request_id)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            events.request.fire(request_type="check_booking_status", name="check_booking_status", response_time=response_time, response_length=0)

    def on_stop(self):
        return
