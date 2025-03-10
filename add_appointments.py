from app import app, db
from models import Appointment
from datetime import datetime, timedelta

def generate_appointments():
    """Manually add Monday-Friday appointment slots from 8:00 AM to 3:00 PM for 30 days."""
    with app.app_context():
        start_time = 8  # 8:00 AM
        end_time = 15   # 3:00 PM
        days_in_future = 30  # Generate for 30 days ahead

        today = datetime.today()
        appointments_created = 0

        for i in range(days_in_future):
            appointment_date = today + timedelta(days=i)
            if appointment_date.weekday() < 5:  # ✅ Only Monday-Friday (0=Monday, 4=Friday)
                for hour in range(start_time, end_time):
                    appointment_datetime = datetime(appointment_date.year, appointment_date.month, appointment_date.day, hour, 0)

                    # ✅ Check if this slot already exists before adding
                    existing_appointment = Appointment.query.filter_by(start=appointment_datetime).first()
                    if not existing_appointment:
                        new_appointment = Appointment(title="Available Slot", start=appointment_datetime)
                        db.session.add(new_appointment)
                        appointments_created += 1

        db.session.commit()
        print(f"✅ {appointments_created} new appointments added for the next 30 days!")

if __name__ == "__main__":
    generate_appointments()
