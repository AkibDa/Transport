document.addEventListener('DOMContentLoaded', function() {
  // Current booking state
  let currentBus = null;
  
  // Step 1: Check Bus Availability
  document.getElementById('check-bus-form').addEventListener('submit', function(e) {
      e.preventDefault();
      const busId = document.getElementById('bus-id').value;
      
      fetch('/api/check_bus', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ bus_id: busId })
      })
      .then(response => {
          if (!response.ok) {
              return response.json().then(err => { throw err; });
          }
          return response.json();
      })
      .then(data => {
          currentBus = data;
          document.getElementById('bus-route').textContent = data.route;
          document.getElementById('bus-seats').textContent = data.available_seats;
          document.getElementById('bus-fare').textContent = data.fare_per_seat;
          document.getElementById('bus-info').classList.remove('hidden');
          
          // Clear any previous error
          const errorDiv = document.querySelector('#step1 .error-message');
          if (errorDiv) errorDiv.remove();
      })
      .catch(error => {
          const errorDiv = document.createElement('div');
          errorDiv.className = 'error-message';
          errorDiv.textContent = error.error || 'Error checking bus availability';
          document.getElementById('check-bus-form').appendChild(errorDiv);
      });
  });
  
  // Proceed to booking step
  document.getElementById('proceed-to-booking').addEventListener('click', function() {
      document.getElementById('step1').classList.add('hidden');
      document.getElementById('step2').classList.remove('hidden');
      document.getElementById('num-seats').focus();
  });
  
  // Step 2: Calculate Fare and Book
  document.getElementById('booking-form').addEventListener('submit', function(e) {
      e.preventDefault();
      const numSeats = document.getElementById('num-seats').value;
      
      if (!currentBus) {
          showError('No bus selected');
          return;
      }
      
      fetch('/api/book', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
              bus_id: currentBus.bus_id,
              num_seats: numSeats
          })
      })
      .then(response => {
          if (!response.ok) {
              return response.json().then(err => { throw err; });
          }
          return response.json();
      })
      .then(data => {
          document.getElementById('total-fare').textContent = data.fare;
          document.getElementById('fare-display').classList.remove('hidden');
          document.getElementById('confirm-booking').classList.remove('hidden');
          
          // Clear any previous error
          const errorDiv = document.querySelector('#step2 .error-message');
          if (errorDiv) errorDiv.remove();
      })
      .catch(error => {
          showError(error.error || 'Error calculating fare');
      });
  });
  
  // Confirm booking
  document.getElementById('confirm-booking').addEventListener('click', function() {
      const numSeats = document.getElementById('num-seats').value;
      
      fetch('/api/confirm_booking', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
              bus_id: currentBus.bus_id,
              num_seats: numSeats
          })
      })
      .then(response => {
          if (!response.ok) {
              return response.json().then(err => { throw err; });
          }
          return response.json();
      })
      .then(data => {
          // Show confirmation
          document.getElementById('step2').classList.add('hidden');
          document.getElementById('step3').classList.remove('hidden');
          document.getElementById('confirmation-message').innerHTML = `
              <p><strong>Booking confirmed!</strong></p>
              <p>Bus ID: ${currentBus.bus_id}</p>
              <p>Route: ${currentBus.route}</p>
              <p>Seats booked: ${numSeats}</p>
              <p>Total fare: Rs${document.getElementById('total-fare').textContent}</p>
              <p>Remaining seats: ${data.new_availability}</p>
          `;
      })
      .catch(error => {
          showError(error.error || 'Error confirming booking');
      });
  });
  
  // Start new booking
  document.getElementById('new-booking').addEventListener('click', function() {
      // Reset everything
      currentBus = null;
      document.getElementById('check-bus-form').reset();
      document.getElementById('booking-form').reset();
      document.getElementById('bus-info').classList.add('hidden');
      document.getElementById('fare-display').classList.add('hidden');
      document.getElementById('confirm-booking').classList.add('hidden');
      document.getElementById('step3').classList.add('hidden');
      document.getElementById('step1').classList.remove('hidden');
  });
  
  function showError(message) {
      // Remove any existing error messages
      const existingError = document.querySelector('.error-message');
      if (existingError) existingError.remove();
      
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.textContent = message;
      document.getElementById('booking-form').appendChild(errorDiv);
  }
});