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

    def get_bus(self, bus_id):
        for bus in self.buses:
            if bus.bus_id == bus_id:
                return bus
        return None

system = TransportSystem()

@app.route('/')
def index():
    return render_template('index.html')

# API endpoints
@app.route('/api/check_bus', methods=['POST'])
def check_bus():
    bus_id = int(request.json.get('bus_id'))
    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Invalid Bus ID'}), 404
    
    return jsonify({
        'bus_id': bus.bus_id,
        'route': bus.route,
        'available_seats': bus.available_seats,
        'fare_per_seat': bus.fare
    })

# All API endpoints in app.py
@app.route('/api/routes')
def get_routes():
    buses = []
    for bus in system.buses:
        buses.append({
            'bus_id': bus.bus_id,
            'route': bus.route,
            'available_seats': bus.available_seats,
            'total_seats': bus.total_seats,
            'fare': bus.fare
        })
    return jsonify(buses)

@app.route('/api/check_bus', methods=['POST'])
def check_bus():
    bus_id = int(request.json.get('bus_id'))
    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Invalid Bus ID'}), 404
    
    return jsonify({
        'bus_id': bus.bus_id,
        'route': bus.route,
        'available_seats': bus.available_seats,
        'fare_per_seat': bus.fare
    })

@app.route('/api/book', methods=['POST'])
def book():
    bus_id = int(request.json.get('bus_id'))
    num_seats = int(request.json.get('num_seats'))
    
    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Invalid Bus ID'}), 404
    
    if num_seats > bus.available_seats:
        return jsonify({'error': 'Not enough seats available'}), 400
    
    fare = bus.get_fare(num_seats)
    return jsonify({
        'fare': fare,
        'available_seats': bus.available_seats
    })

@app.route('/api/book', methods=['POST'])
def book():
    bus_id = int(request.json.get('bus_id'))
    num_seats = int(request.json.get('num_seats'))
    
    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Invalid Bus ID'}), 404
    
    if num_seats > bus.available_seats:
        return jsonify({'error': 'Not enough seats available'}), 400
    
    # Calculate fare before booking to show user
    fare = bus.get_fare(num_seats)
    
    # Only book if user confirms (we'll handle this in frontend)
    return jsonify({
        'fare': fare,
        'available_seats': bus.available_seats
    })

@app.route('/api/confirm_booking', methods=['POST'])
def confirm_booking():
    bus_id = int(request.json.get('bus_id'))
    num_seats = int(request.json.get('num_seats'))
    
    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Invalid Bus ID'}), 404
    
    success = bus.book_tickets(num_seats)
    if not success:
        return jsonify({'error': 'Booking failed'}), 400
    
    return jsonify({
        'message': f'Successfully booked {num_seats} seat(s)',
        'new_availability': bus.available_seats
    })

if __name__ == '__main__':
    app.run(debug=True)