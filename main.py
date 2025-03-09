class Bus:

  def __init__(self, bus_id, route, total_seats, fare):

    self.bus_id = bus_id
    self.route = route 
    self.total_seats = total_seats
    self.available_seats = total_seats
    self.fare = fare 

  def check_availability(self):

    return self.available_seats

  def book_tickets(self, num_seats):

    if num_seats > self.available_seats:
      return False

    self.available_seats -= num_seats
    return True

  def get_fare(self, num_seats):

    return self.fare * num_seats

class TransportSystem:

  def __init__(self):

    self.buses = [
      Bus(101, "Route A: City Center to Airport", 40, 10),
      Bus(102, "Route B: Downtown to Mall", 30, 7),
      Bus(103, "Route A: Train Station to University", 35, 8),
    ]

  def view_routes(self):

    print("\nAvailable Bus Routes:")

    for bus in self.buses:
      print(f"{bus.bus_id}: {bus.route} (Seats: {bus.available_seats}/{bus.total_seats}, Fare: Rs{bus.fare})") 

  def check_seat_availability(self, bus_id):

    for bus in self.buses:
      if bus.bus_id == bus_id:
        return bus.check_availability()
    return None

  def book_ticket(self, bus_id, num_seats):

    for bus in self.buses:
      if bus.bus_id == bus_id:
        return bus.book_tickets(num_seats)
    return None
  
  def get_fare_estimate(self, bus_id, num_seats):

    for bus in self.buses:
      if bus.bus_id == bus_id:
        return bus.get_fare(num_seats)
    return None

def main():

  system = TransportSystem()

  while True:

    print("\nPublic Transport System")
    print("1. View Available Routes")
    print("2. Check Seat Availability")
    print("3. Book a Ticket")
    print("4. Get Fare Estimation")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
      system.view_routes()
    elif choice == '2':
      bus_id = int(input("Enter Bus ID: "))
      seats = system.check_seat_availability(bus_id)
      if seats is not None:
        print(f"Available seats: {seats}")
      else:
        print("Invalid Bus ID!")
    elif choice == '3':
      bus_id = int(input("Enter Bus ID: "))
      num_seats = int(input("Enter number of seats: "))
      success = system.book_ticket(bus_id, num_seats)
      if success:
        print(f"{num_seats} seat(s) booked successfully!")
      else:
        print("Booking failed. Not enough seats or invalid Bus ID.")
    elif choice == '4':
      bus_id = int(input("Enter Bus ID: "))
      num_seats = int(input("Enter number of seats: "))
      fare = system.get_fare_estimate(bus_id, num_seats)
      if fare is not None:
        print(f"Estimate Fare: Rs{fare}")
      else:
        print("Invalid Bus ID!")
    elif choice == '5':
      print("Exiting... Safe travels!")
      break
    else:
      print("Invalid choice! Please try again.")

if __name__ == "__main__":
  main()