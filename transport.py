from dataclasses import dataclass, field

@dataclass
class Bus:
    bus_id: int
    route: str
    total_seats: int
    fare: float
    available_seats: int = field(init=False)

    def __post_init__(self):
        self.available_seats = self.total_seats

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
            Bus(103, "Route C: Train Station to University", 35, 8),
        ]

    def get_bus(self, bus_id):
        return next((bus for bus in self.buses if bus.bus_id == bus_id), None)

    def add_bus(self, bus_id, route, total_seats, fare):
        if self.get_bus(bus_id):
            return False  # Bus with the same ID exists
        self.buses.append(Bus(bus_id, route, total_seats, fare))
        return True


# Create a single instance for the app
system = TransportSystem()
