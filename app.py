import os
import smtplib 
from email.message import EmailMessage

from flask import Flask, render_template, url_for, jsonify, request
from flask_mail import Mail, Message 
from models import db, Appointment
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Load all configurations from Config

mail = Mail(app)

db.init_app(app)

def generate_appointments():
    """Create Monday-Friday appointment slots from 8:00 AM to 3:00 PM for 30 days."""
    with app.app_context():
        db.session.query(Appointment).delete()  
        start_time = 8  # 8:00 AM
        end_time = 15   # 3:00 PM
        days_in_future = 30  # How many days ahead to generate

        today = datetime.today()

        for i in range(days_in_future):
            appointment_date = today + timedelta(days=i)
            if appointment_date.weekday() < 5:  # ✅ Only Monday-Friday (0=Monday, 4=Friday)
                for hour in range(start_time, end_time):
                    appointment_datetime = datetime(appointment_date.year, appointment_date.month, appointment_date.day, hour, 0)
                    db.session.add(Appointment(title="Available Slot", start=appointment_datetime))

        db.session.commit()
        print("Appointments generated successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, phone, email, message]):
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

    subject = "New Contact Form Submission"
    email_body = f"""
    You have a new contact form submission:

    Name: {name}
    Email: {email}
    Phone: {phone}
    
    Message:
    {message}
    """

    try:
        msg = EmailMessage()
        msg.set_content(email_body)
        msg["Subject"] = subject
        msg["From"] = app.config['MAIL_USERNAME']
        msg["To"] = app.config['MAIL_USERNAME']  # Sending to yourself

        # Use TLS connection (matches your config)
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.starttls()  # Enable TLS encryption
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)

        return jsonify({'status': 'success', 'message': 'Thank you! Your message has been sent.'})

    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': f'Could not send email: {str(e)}'}), 500

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
        generate_appointments()
    app.run(debug=True)