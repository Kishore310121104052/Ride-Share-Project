import uuid
import random
from datetime import datetime


users = []
rides = []
ride_requests = []

class User:
    def __init__(self, name, role):
        self.id = uuid.uuid4()
        self.name = name
        self.role = role

class Rider(User):
    def __init__(self, name):
        super().__init__(name, "Rider")
    
    def search_rides(self):
        destination = input("Enter destination: ")
        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (HH:MM): ")
        
        print("\nAvailable Rides:")
        for ride in rides:
            if ride.destination == destination and ride.date == date:
                print(f"Ride ID: {ride.id} | Driver: {ride.driver.name} | Time: {ride.time} | Seats: {ride.seats_available}")

    def request_ride(self):
        ride_id = input("Enter Ride ID to request: ")
        selected_ride = next((ride for ride in rides if str(ride.id) == ride_id), None)
        
        if selected_ride and selected_ride.seats_available > 0:
            ride_requests.append({
                "ride_id": selected_ride.id,
                "rider_id": self.id,
                "status": "Pending"
            })
            print("Ride request sent to the driver!")
        else:
            print("Invalid Ride ID or no seats available.")

    def view_requested_rides(self):
        print("\nYour Requested Rides:")
        for request in ride_requests:
            if request["rider_id"] == self.id:
                ride = next((ride for ride in rides if ride.id == request["ride_id"]), None)
                if ride:
                    print(f"Ride to {ride.destination} on {ride.date} at {ride.time} - Status: {request['status']}")

class Driver(User):
    def __init__(self, name):
        super().__init__(name, "Driver")
    
    def post_ride(self):
        destination = input("Enter destination: ")
        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (HH:MM): ")
        seats = int(input("Enter available seats: "))
        
        ride = Ride(self, destination, date, time, seats)
        rides.append(ride)
        print("Ride posted successfully!")
    
    def view_ride_requests(self):
        print("\nRide Requests:")
        for request in ride_requests:
            ride = next((ride for ride in rides if ride.id == request["ride_id"]), None)
            if ride and ride.driver.id == self.id:
                rider = next((user for user in users if user.id == request["rider_id"]), None)
                print(f"Request from {rider.name} for Ride to {ride.destination} on {ride.date} at {ride.time}")
    
    def approve_request(self):
        rider_name = input("Enter Rider name to approve: ")
        rider = next((user for user in users if user.name == rider_name and user.role == "Rider"), None)
        
        if rider:
            for request in ride_requests:
                if request["rider_id"] == rider.id:
                    request["status"] = "Approved"
                    ride = next((ride for ride in rides if ride.id == request["ride_id"]), None)
                    ride.seats_available -= 1
                    print("Ride request approved!")
        else:
            print("Rider not found.")

class Administrator(User):
    def __init__(self, name):
        super().__init__(name, "Admin")
    
    def manage_users(self):
        print("\nUser Management:")
        action = input("Enter 'add' to add user, 'remove' to remove user: ")
        if action == "add":
            name = input("Enter name: ")
            role = input("Enter role (Rider/Driver): ")
            if role == "Rider":
                users.append(Rider(name))
            elif role == "Driver":
                users.append(Driver(name))
            print(f"User {name} added as {role}.")
        elif action == "remove":
            name = input("Enter name to remove: ")
            user = next((user for user in users if user.name == name), None)
            if user:
                users.remove(user)
                print(f"User {name} removed.")
            else:
                print("User not found.")
    
    def generate_reports(self):
        print("\nReport Generation:")
        print(f"Total Rides: {len(rides)}")
        print(f"Total Users: {len(users)}")
        print(f"Total Ride Requests: {len(ride_requests)}")
        approved_requests = len([req for req in ride_requests if req['status'] == 'Approved'])
        print(f"Approved Ride Requests: {approved_requests}")

class Ride:
    def __init__(self, driver, destination, date, time, seats):
        self.id = uuid.uuid4()
        self.driver = driver
        self.destination = destination
        self.date = date
        self.time = time
        self.seats_available = seats

def login():
    print("\n--- Login ---")
    name = input("Enter your name: ")
    user = next((user for user in users if user.name == name), None)
    
    if not user:
        print("User not found. Please contact the administrator.")
        return None
    return user

def main():
    print("Welcome to the RideShare Application")
    
    # Adding sample users and rides
    admin = Administrator("Admin")
    users.append(admin)
    
    rider_kishore = Rider("Kishore")
    users.append(rider_kishore)
    
    driver_dhilip = Driver("Dhilip")
    users.append(driver_dhilip)
    
    # Dhilip posts a ride
    ride_to_college = Ride(driver_dhilip, "AIHT College", "2004-09-07", "08:30", 3)
    rides.append(ride_to_college)
    
    while True:
        user = login()
        if user:
            if user.role == "Rider":
                while True:
                    print("\n--- Rider Menu ---")
                    print("1. Search Rides\n2. Request Ride\n3. View Requested Rides\n4. Logout")
                    choice = input("Choose an option: ")
                    if choice == "1":
                        user.search_rides()
                    elif choice == "2":
                        user.request_ride()
                    elif choice == "3":
                        user.view_requested_rides()
                    elif choice == "4":
                        break
            elif user.role == "Driver":
                while True:
                    print("\n--- Driver Menu ---")
                    print("1. Post a Ride\n2. View Ride Requests\n3. Approve Request\n4. Logout")
                    choice = input("Choose an option: ")
                    if choice == "1":
                        user.post_ride()
                    elif choice == "2":
                        user.view_ride_requests()
                    elif choice == "3":
                        user.approve_request()
                    elif choice == "4":
                        break
            elif user.role == "Admin":
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Manage Users\n2. Generate Reports\n3. Logout")
                    choice = input("Choose an option: ")
                    if choice == "1":
                        user.manage_users()
                    elif choice == "2":
                        user.generate_reports()
                    elif choice == "3":
                        break

if __name__ == "__main__":
    main()
