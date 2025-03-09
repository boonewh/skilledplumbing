from flask import Flask, render_template, url_for, jsonify, request
from models import db, Appointment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/api/appointments')
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])

@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.json
    appointment = Appointment.query.get(data['id'])
    if appointment and not appointment.booked:
        appointment.booked = True
        appointment.title = f"Booked by {data['name']}"  # Update title with name
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Appointment not available or already booked'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
