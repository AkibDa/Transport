document.addEventListener('DOMContentLoaded', function() {
  // Load routes when page loads
  loadRoutes();
  
  // Set up form event listeners
  document.getElementById('availability-form').addEventListener('submit', checkAvailability);
  document.getElementById('book-form').addEventListener('submit', bookTickets);
  document.getElementById('fare-form').addEventListener('submit', calculateFare);
});

function loadRoutes() {
  fetch('/api/routes')
      .then(response => response.json())
      .then(data => {
          const container = document.getElementById('routes-container');
          
          if (data.length === 0) {
              container.innerHTML = '<p>No routes available</p>';
              return;
          }
          
          let html = `
              <table>
                  <thead>
                      <tr>
                          <th>Bus ID</th>
                          <th>Route</th>
                          <th>Available Seats</th>
                          <th>Fare (Rs)</th>
                      </tr>
                  </thead>
                  <tbody>
          `;
          
          data.forEach(bus => {
              html += `
                  <tr>
                      <td>${bus.bus_id}</td>
                      <td>${bus.route}</td>
                      <td>${bus.available_seats}/${bus.total_seats}</td>
                      <td>${bus.fare}</td>
                  </tr>
              `;
          });
          
          html += `</tbody></table>`;
          container.innerHTML = html;
      })
      .catch(error => {
          console.error('Error loading routes:', error);
          document.getElementById('routes-container').innerHTML = 
              '<p class="error">Error loading routes. Please try again.</p>';
      });
}

function checkAvailability(e) {
  e.preventDefault();
  const busId = document.getElementById('avail-bus-id').value;
  const resultDiv = document.getElementById('availability-result');
  
  fetch('/api/check_availability', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ bus_id: busId })
  })
  .then(response => response.json())
  .then(data => {
      if (data.available_seats === null) {
          resultDiv.innerHTML = `<p class="error">Invalid Bus ID</p>`;
      } else {
          resultDiv.innerHTML = `<p class="success">Available seats: ${data.available_seats}</p>`;
      }
  })
  .catch(error => {
      console.error('Error:', error);
      resultDiv.innerHTML = `<p class="error">Error checking availability</p>`;
  });
}

function bookTickets(e) {
  e.preventDefault();
  const busId = document.getElementById('book-bus-id').value;
  const numSeats = document.getElementById('num-seats').value;
  const resultDiv = document.getElementById('book-result');
  
  fetch('/api/book', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
          bus_id: busId,
          num_seats: numSeats
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          resultDiv.innerHTML = `
              <p class="success">
                  ${numSeats} seat(s) booked successfully!
              </p>
          `;
          // Refresh routes to show updated availability
          loadRoutes();
      } else {
          resultDiv.innerHTML = `
              <p class="error">
                  Booking failed. Not enough seats or invalid Bus ID.
              </p>
          `;
      }
  })
  .catch(error => {
      console.error('Error:', error);
      resultDiv.innerHTML = `<p class="error">Error processing booking</p>`;
  });
}

function calculateFare(e) {
  e.preventDefault();
  const busId = document.getElementById('fare-bus-id').value;
  const numSeats = document.getElementById('fare-num-seats').value;
  const resultDiv = document.getElementById('fare-result');
  
  fetch('/api/fare', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
          bus_id: busId,
          num_seats: numSeats
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.fare === null) {
          resultDiv.innerHTML = `<p class="error">Invalid Bus ID</p>`;
      } else {
          resultDiv.innerHTML = `
              <p class="success">
                  Estimated fare for ${numSeats} seat(s): Rs${data.fare}
              </p>
          `;
      }
  })
  .catch(error => {
      console.error('Error:', error);
      resultDiv.innerHTML = `<p class="error">Error calculating fare</p>`;
  });
}