from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, db

# Firebase Setup
cred = credentials.Certificate("iot-14055-firebase-adminsdk-i4dbt-eba7beb6a1.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-14055-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

# Route
@app.route('/')
def index():
    return render_template('index.html')

# API route to get parking slot data
@app.route('/api/parking_slots', methods=['GET'])
def get_parking_slots():
    ref = db.reference('ParkingSlots')
    slots = ref.get()
    return jsonify(slots), 200

# API route to update a parking slot status
@app.route('/api/update_slot', methods=['POST'])
def update_slot():
    data = request.json
    slot_id = data.get('slot_id')
    status = data.get('status')  # 'occupied' or 'vacant'

    if slot_id and status in ['occupied', 'vacant']:
        ref = db.reference(f'ParkingSlots/{slot_id}')
        ref.set({'status': status})
        return jsonify({"message": f"Slot {slot_id} updated to {status}"}), 200
    else:
        return jsonify({"message": "Invalid slot ID or status"}), 400

# route to book parking slots
@app.route('/api/book_slot', methods=['POST'])
def book_slot():
    try:
        data = request.json
        print(f"Received Data: {data}")  # Debug incoming data

        slot_id = data.get('slot_id')
        if not slot_id:
            return jsonify({"message": "Slot ID is required"}), 400

        # Log the slot being updated
        print(f"Updating slot: {slot_id}")

        # Update the slot status to 'occupied' in Firebase
        ref = db.reference(f'ParkingSlots/{slot_id}')
        ref.set({"status": "occupied"})  # Update Firebase

        return jsonify({"message": f"Slot {slot_id} successfully booked!"}), 200
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        return jsonify({"message": "Failed to book slot"}), 500



@app.route('/api/reset_slot', methods=['POST'])
def reset_slot():
    try:
        data = request.json
        print(f"Received Data: {data}")  # Debug incoming data

        slot_id = data.get('slot_id')
        if not slot_id:
            return jsonify({"message": "Slot ID is required"}), 400

        # Log the slot being updated
        print(f"Updating slot: {slot_id}")

        # Update the slot status to 'occupied' in Firebase
        ref = db.reference(f'ParkingSlots/{slot_id}')
        ref.set({"status": "vacant"})  # Update Firebase

        return jsonify({"message": f"Slot {slot_id} successfully released!"}), 200
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        return jsonify({"message": "Failed to book slot"}), 500



if __name__ == '__main__':
    app.run(debug=True)



