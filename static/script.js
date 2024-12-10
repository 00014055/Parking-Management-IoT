document.addEventListener('DOMContentLoaded', () => {
    const parkingLot = document.getElementById('parking-lot');

    // Fetch parking slots data from API
    function fetchSlots() {
        fetch('/api/parking_slots')
            .then(response => response.json())
            .then(data => {
                renderParkingLot(data);
            })
            .catch(err => console.error('Error fetching slots:', err));
    }

    // Render parking slots
    function renderParkingLot(slots) {
        parkingLot.innerHTML = '';
        for (let slot in slots) {
            const slotData = slots[slot];
            const slotDiv = document.createElement('div');
            slotDiv.className = `slot ${slotData.status} ${slotData.reserved ? 'reserved' : ''}`;
            slotDiv.innerHTML = `
                <h3>${slot}</h3>
                <p>Status: ${slotData.status}</p>
                ${slotData.status === 'vacant' ? `<button class="book" onclick="bookSlot('${slot}')">Book</button>` : ''}
                ${slotData.status === 'occupied' ? `<button class="reset" onclick="resetSlot('${slot}')">Reset</button>` : ''}
            `;
            parkingLot.appendChild(slotDiv);
        }
    }

    // Book slot
    window.bookSlot = function(slot) {
        fetch('/api/book_slot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slot_id: slot })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                fetchSlots();
            })
            .catch(err => console.error('Error booking slot:', err));
    };

    // Reset slot
    window.resetSlot = function(slot) {
        fetch('/api/reset_slot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slot_id: slot })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                fetchSlots();
            })
            .catch(err => console.error('Error resetting slot:', err));
    };

    fetchSlots();
});
