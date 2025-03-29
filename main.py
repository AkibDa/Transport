from flask import Flask, render_template, request, jsonify
from transport import system  # Import business logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/routes')
def get_routes():
    buses = [
        {
            'bus_id': bus.bus_id,
            'route': bus.route,
            'available_seats': bus.available_seats,
            'total_seats': bus.total_seats,
            'fare': bus.fare
        }
        for bus in system.buses
    ]
    return jsonify(buses)


@app.route('/api/check_bus', methods=['POST'])
def check_bus():
    try:
        bus_id = int(request.json.get('bus_id'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid bus ID format'}), 400

    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Bus not found'}), 404

    return jsonify({
        'bus_id': bus.bus_id,
        'route': bus.route,
        'available_seats': bus.available_seats,
        'fare_per_seat': bus.fare
    })


@app.route('/api/book', methods=['POST'])
def book():
    try:
        bus_id = int(request.json.get('bus_id'))
        num_seats = int(request.json.get('num_seats'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input format'}), 400

    bus = system.get_bus(bus_id)
    if not bus:
        return jsonify({'error': 'Bus not found'}), 404

    if not bus.book_tickets(num_seats):
        return jsonify({'error': 'Not enough seats available'}), 400

    return jsonify({
        'message': f'Booked {num_seats} seats successfully!',
        'new_availability': bus.available_seats,
        'total_fare': bus.get_fare(num_seats)
    })


@app.route('/api/add_bus', methods=['POST'])
def add_bus():
    try:
        data = request.json
        bus_id = int(data.get('bus_id'))
        route = data.get('route')
        total_seats = int(data.get('total_seats'))
        fare = float(data.get('fare'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input format'}), 400

    if not route or total_seats <= 0 or fare <= 0:
        return jsonify({'error': 'Invalid bus details'}), 400

    if not system.add_bus(bus_id, route, total_seats, fare):
        return jsonify({'error': 'Bus ID already exists'}), 400

    return jsonify({'message': 'Bus added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
