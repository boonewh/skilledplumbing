from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Available Slot")
    start = db.Column(db.DateTime, nullable=False)  # ✅ Store as DateTime
    booked = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Convert model data to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title if self.booked else "Available Slot",
            'start': self.start.strftime("%Y-%m-%dT%H:%M:%S"),  # ✅ Format for FullCalendar
            'color': '#ff0000' if self.booked else '#008000'  # Red if booked, green if available
        }
