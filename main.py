from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
def home():
    return render_template('index.html')

@app.route('/routes')
def routes():
    buses = system.view_routes()
    return render_template('routes.html', buses=buses)

@app.route('/availability', methods=['GET', 'POST'])
def availability():
    if request.method == 'POST':
        bus_id = int(request.form['bus_id'])
        seats = system.check_seat_availability(bus_id)
        if seats is not None:
            flash(f"Available seats on Bus {bus_id}: {seats}", 'success')
        else:
            flash("Invalid Bus ID!", 'error')
        return redirect(url_for('availability'))
    return render_template('availability.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        bus_id = int(request.form['bus_id'])
        num_seats = int(request.form['num_seats'])
        success = system.book_ticket(bus_id, num_seats)
        if success:
            flash(f"{num_seats} seat(s) on Bus {bus_id} booked successfully!", 'success')
        else:
            flash("Booking failed. Not enough seats or invalid Bus ID.", 'error')
        return redirect(url_for('book'))
    return render_template('book.html')

@app.route('/fare', methods=['GET', 'POST'])
def fare():
    if request.method == 'POST':
        bus_id = int(request.form['bus_id'])
        num_seats = int(request.form['num_seats'])
        fare = system.get_fare_estimate(bus_id, num_seats)
        if fare is not None:
            flash(f"Estimated fare for {num_seats} seat(s) on Bus {bus_id}: Rs{fare}", 'success')
        else:
            flash("Invalid Bus ID!", 'error')
        return redirect(url_for('fare'))
    return render_template('fare.html')

if __name__ == '__main__':
    app.run(debug=True)