import os
from flask import Flask, render_template, url_for, jsonify, request
from flask_mail import Mail, Message
from models import db, Appointment
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
db.init_app(app)

# -------------------- APPOINTMENT GENERATION --------------------

def generate_appointments():
    """Create Monday-Friday appointment slots from 8:00 AM to 3:00 PM for 30 days."""
    with app.app_context():
        db.session.query(Appointment).delete()
        start_time = 8
        end_time = 15
        days_in_future = 30
        today = datetime.today()

        for i in range(days_in_future):
            appointment_date = today + timedelta(days=i)
            if appointment_date.weekday() < 5:
                for hour in range(start_time, end_time):
                    appointment_datetime = datetime(appointment_date.year, appointment_date.month, appointment_date.day, hour, 0)
                    db.session.add(Appointment(title="Available Slot", start=appointment_datetime))

        db.session.commit()
        print("Appointments generated successfully!")

# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

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
        appointment.title = "Appointment Scheduled"
        appointment.name = data['name']
        appointment.address = data['address']
        appointment.city = data['city']
        appointment.phone = data['phone']
        appointment.email = data['email']
        appointment.heater_type = data['heaterType'] 
        db.session.commit()

        # Common email body
        appointment_time = appointment.start.strftime('%Y-%m-%d %I:%M %p')
        body = f"""
        A new appointment has been booked:

        Name: {appointment.name}
        Address: {appointment.address}
        City: {appointment.city}
        Phone: {appointment.phone}
        Email: {appointment.email}
        Time: {appointment_time}
        Water Heater Type: {appointment.heater_type if appointment.heater_type else 'Not specified'}
        """

        try:
            # 📤 Internal notification
            internal_msg = Message(
                subject="New Appointment Scheduled",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[
                    'stephen@skilledwaterheater.com',
                    'boonewh@pathsixdesigns.com'
                ]
            )
            internal_msg.body = body
            mail.send(internal_msg)

            # 📤 Customer confirmation
            customer_msg = Message(
                subject="Appointment Confirmation - Skilled Plumbing",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[appointment.email]
            )
            customer_msg.body = f"""Hi {appointment.name},

Thank you for scheduling your appointment with Skilled Plumbing!

Here are the details of your appointment:

Date & Time: {appointment_time}
Address: {appointment.address}, {appointment.city}
Phone: {appointment.phone}
Water Heater Type: {appointment.heater_type if appointment.heater_type else 'Not specified'}

If you have any questions, feel free call us at (432) 553-2702.

- Skilled Plumbing Team
"""
            mail.send(customer_msg)

            return jsonify({'status': 'success'})
        except Exception as e:
            print(f"Email error: {e}")
            return jsonify({'status': 'error', 'message': 'Booking saved, but email failed.'}), 500

    return jsonify({'status': 'error', 'message': 'Appointment not available or already booked'}), 400

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, phone, email, message]):
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    subject = "New Contact Form Submission"
    body = f"""
    You have a new contact form submission:

    Name: {name}
    Email: {email}
    Phone: {phone}

    Message:
    {message}
    """

    try:
        msg = Message(
            subject,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = body
        msg.reply_to = email  # ✅ reply-to user's actual email
        mail.send(msg)

        return jsonify({'status': 'success', 'message': 'Thank you! Your message has been sent.'})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': f'Could not send email: {str(e)}'}), 500

# -------------------- STARTUP --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        generate_appointments()
    app.run(debug=True)
