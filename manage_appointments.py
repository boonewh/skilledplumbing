import os
import sys
from datetime import datetime, timedelta, time
from flask import Flask
from models import db, Appointment

# This script should be placed in the same directory as your Flask app
# Import your app configuration
from app import app

def cleanup_morning_slots():
    """Remove 8am, 9am, and 10am slots from the current day (using local time)"""
    with app.app_context():
        today = datetime.today().date()
        # Skip the time check - execute whenever this function is called
        # Since we're running this as a scheduled task, we'll control
        # execution by scheduling, not by checking the current time
        
        # Times to remove (8am, 9am, 10am)
        hours_to_remove = [8, 9, 10]
        
        # Get today's appointments in the specified hours
        for hour in hours_to_remove:
            slot_time = datetime.combine(today, time(hour=hour))
            appointment = Appointment.query.filter_by(start=slot_time).first()
            
            if appointment and appointment.title == "Available Slot" and not appointment.booked:
                db.session.delete(appointment)
        
        db.session.commit()
        print(f"✅ Removed available morning slots ({hours_to_remove}) for {today}")

def cleanup_midday_slots():
    """Remove 11am, 12pm, and 1pm slots from the current day (using local time)"""
    with app.app_context():
        today = datetime.today().date()
        # Skip the time check - execute whenever this function is called
        
        # Times to remove (11am, 12pm, 1pm)
        hours_to_remove = [11, 12, 13]
        
        # Get today's appointments in the specified hours
        for hour in hours_to_remove:
            slot_time = datetime.combine(today, time(hour=hour))
            appointment = Appointment.query.filter_by(start=slot_time).first()
            
            if appointment and appointment.title == "Available Slot" and not appointment.booked:
                db.session.delete(appointment)
        
        db.session.commit()
        print(f"✅ Removed available midday slots ({hours_to_remove}) for {today}")

def cleanup_afternoon_slots():
    """Remove 2pm and 3pm slots from the current day (using local time)"""
    with app.app_context():
        today = datetime.today().date()
        # Skip the time check - execute whenever this function is called
        
        # Times to remove (2pm, 3pm)
        hours_to_remove = [14, 15]
        
        # Get today's appointments in the specified hours
        for hour in hours_to_remove:
            slot_time = datetime.combine(today, time(hour=hour))
            appointment = Appointment.query.filter_by(start=slot_time).first()
            
            if appointment and appointment.title == "Available Slot" and not appointment.booked:
                db.session.delete(appointment)
        
        db.session.commit()
        print(f"✅ Removed available afternoon slots ({hours_to_remove}) for {today}")

def cleanup_all_remaining_slots():
    """Remove all remaining slots for today (using local time)"""
    with app.app_context():
        today = datetime.today().date()
        # Skip the time check - execute whenever this function is called
        
        # Get all today's appointments
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)
        
        # Find all available slots for today
        available_slots = Appointment.query.filter(
            Appointment.start >= start_of_day,
            Appointment.start <= end_of_day,
            Appointment.title == "Available Slot",
            Appointment.booked == False
        ).all()
        
        # Delete all available slots
        for slot in available_slots:
            db.session.delete(slot)
        
        db.session.commit()
        print(f"✅ Removed all remaining available slots for {today}")

def add_new_day():
    """Add a new day of appointments at the end of the current schedule"""
    with app.app_context():
        # Find the latest appointment date in the system
        latest_appointment = Appointment.query.order_by(Appointment.start.desc()).first()
        
        if latest_appointment:
            latest_date = latest_appointment.start.date()
            # Add appointments for the next day after the latest date
            next_date = latest_date + timedelta(days=1)
            
            # Skip to the next weekday if it's a weekend
            while next_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                next_date += timedelta(days=1)
            
            # Add slots from 8am to 3pm
            start_time = 8  # 8:00 AM
            end_time = 15   # 3:00 PM (15:00)
            
            appointments_created = 0
            
            for hour in range(start_time, end_time):
                appointment_datetime = datetime.combine(next_date, time(hour=hour))
                
                # Check if this slot already exists
                existing_appointment = Appointment.query.filter_by(start=appointment_datetime).first()
                if not existing_appointment:
                    new_appointment = Appointment(title="Available Slot", start=appointment_datetime)
                    db.session.add(new_appointment)
                    appointments_created += 1
            
            db.session.commit()
            print(f"✅ Added {appointments_created} new appointment slots for {next_date}")
        else:
            print("⚠️ No existing appointments found. Cannot determine the latest date.")

def main():
    """Main function to handle different operations based on command-line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python manage_appointments.py [morning|midday|afternoon|noon|add-day|all]")
        return
    
    operation = sys.argv[1].lower()
    
    if operation == "morning":
        cleanup_morning_slots()
    elif operation == "midday":
        cleanup_midday_slots()
    elif operation == "afternoon":
        cleanup_afternoon_slots()
    elif operation == "noon":
        cleanup_all_remaining_slots()
        add_new_day()  # After removing all slots at noon, add a new day
    elif operation == "add-day":
        add_new_day()
    elif operation == "all":
        # Run all operations in sequence - use this for testing
        cleanup_morning_slots()
        cleanup_midday_slots()
        cleanup_afternoon_slots()
        cleanup_all_remaining_slots()
        add_new_day()
    else:
        print(f"Unknown operation: {operation}")
        print("Usage: python manage_appointments.py [morning|midday|afternoon|noon|add-day|all]")

if __name__ == "__main__":
    main()