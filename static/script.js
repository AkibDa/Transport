document.addEventListener('DOMContentLoaded', () => {
    let currentBus = null;
    loadAvailableBuses();

    // Selectors
    const busForm = document.getElementById('check-bus-form');
    const bookingForm = document.getElementById('booking-form');
    const confirmBookingBtn = document.getElementById('confirm-booking');
    const proceedToBookingBtn = document.getElementById('proceed-to-booking');
    const newBookingBtn = document.getElementById('new-booking');

    busForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const busId = document.getElementById('bus-id').value;
        
        try {
            currentBus = await fetchData('/api/check_bus', 'POST', { bus_id: busId });
            displayBusInfo(currentBus);
        } catch (error) {
            showError(error.error || 'Error checking bus availability.');
        }
    });

    proceedToBookingBtn.addEventListener('click', () => {
        toggleSteps('step1', 'step2');
        document.getElementById('num-seats').focus();
    });

    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const numSeats = parseInt(document.getElementById('num-seats').value, 10);
        
        if (!currentBus) return showError('No bus selected. Please go back and select a bus.');
        if (numSeats <= 0) return showError('Please enter a valid number of seats.');

        try {
            const data = await fetchData('/api/book', 'POST', {
                bus_id: currentBus.bus_id,
                num_seats: numSeats
            });
            document.getElementById('total-fare').textContent = data.fare;
            document.getElementById('fare-display').classList.remove('hidden');
            confirmBookingBtn.classList.remove('hidden');
        } catch (error) {
            showError(error.error || 'Error calculating fare. Please try again.');
        }
    });

    confirmBookingBtn.addEventListener('click', async () => {
        const numSeats = parseInt(document.getElementById('num-seats').value, 10);

        try {
            const data = await fetchData('/api/confirm_booking', 'POST', {
                bus_id: currentBus.bus_id,
                num_seats: numSeats
            });
            toggleSteps('step2', 'step3');
            displayConfirmation(data, numSeats);
            loadAvailableBuses();
        } catch (error) {
            showError(error.error || 'Error confirming booking.');
        }
    });

    newBookingBtn.addEventListener('click', resetBookingProcess);

    async function loadAvailableBuses() {
        try {
            const data = await fetchData('/api/routes');
            renderBusTable(data);
        } catch (error) {
            document.getElementById('buses-list').innerHTML = '<tr><td colspan="4">Error loading bus information. Please refresh.</td></tr>';
        }
    }

    async function fetchData(url, method = 'GET', body = null) {
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (body) options.body = JSON.stringify(body);
        const response = await fetch(url, options);
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
    }

    function displayBusInfo(bus) {
        document.getElementById('bus-route').textContent = bus.route;
        document.getElementById('bus-seats').textContent = bus.available_seats;
        document.getElementById('bus-fare').textContent = bus.fare_per_seat;
        document.getElementById('bus-info').classList.remove('hidden');
        clearError();
    }

    function renderBusTable(buses) {
        const busesList = document.getElementById('buses-list');
        busesList.innerHTML = buses.length ? buses.map(bus => `
            <tr>
                <td>${bus.bus_id}</td>
                <td>${bus.route}</td>
                <td>${bus.available_seats}/${bus.total_seats}</td>
                <td>Rs${bus.fare}</td>
            </tr>`).join('') : '<tr><td colspan="4">No buses available at the moment</td></tr>';
    }

    function showError(message) {
        clearError();
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        bookingForm.appendChild(errorDiv);
    }

    function clearError() {
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
    }

    function toggleSteps(hideStep, showStep) {
        document.getElementById(hideStep).classList.add('hidden');
        document.getElementById(showStep).classList.remove('hidden');
    }

    function displayConfirmation(data, numSeats) {
        document.getElementById('confirmation-message').innerHTML = `
            <p><strong>✅ Booking confirmed!</strong></p>
            <p><strong>Bus ID:</strong> ${currentBus.bus_id}</p>
            <p><strong>Route:</strong> ${currentBus.route}</p>
            <p><strong>Seats booked:</strong> ${numSeats}</p>
            <p><strong>Total fare:</strong> Rs${document.getElementById('total-fare').textContent}</p>
            <p><strong>Remaining seats:</strong> ${data.new_availability}</p>
        `;
    }

    function resetBookingProcess() {
        currentBus = null;
        busForm.reset();
        bookingForm.reset();
        document.getElementById('bus-info').classList.add('hidden');
        document.getElementById('fare-display').classList.add('hidden');
        confirmBookingBtn.classList.add('hidden');
        toggleSteps('step3', 'step1');
    }
});
