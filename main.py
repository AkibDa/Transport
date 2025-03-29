from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
            Bus(103, "Route C: Train Station to University", 35, 8),
        ]

    def view_routes(self):
        return self.buses

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

system = TransportSystem()

@app.route('/')
def index():
    return render_template('index.html')

# API endpoints for AJAX calls
@app.route('/api/routes')
def get_routes():
    buses = system.view_routes()
    return jsonify([{
        'bus_id': bus.bus_id,
        'route': bus.route,
        'available_seats': bus.available_seats,
        'total_seats': bus.total_seats,
        'fare': bus.fare
    } for bus in buses])

@app.route('/api/check_availability', methods=['POST'])
def check_availability():
    data = request.get_json()
    bus_id = int(data['bus_id'])
    seats = system.check_seat_availability(bus_id)
    return jsonify({'available_seats': seats})

@app.route('/api/book', methods=['POST'])
def book():
    data = request.get_json()
    bus_id = int(data['bus_id'])
    num_seats = int(data['num_seats'])
    success = system.book_ticket(bus_id, num_seats)
    return jsonify({'success': success})

@app.route('/api/fare', methods=['POST'])
def fare():
    data = request.get_json()
    bus_id = int(data['bus_id'])
    num_seats = int(data['num_seats'])
    fare = system.get_fare_estimate(bus_id, num_seats)
    return jsonify({'fare': fare})

if __name__ == '__main__':
    app.run(debug=True)