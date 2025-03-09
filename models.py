from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ This initializes the database

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Available Slot")
    start = db.Column(db.String(50), nullable=False)  # Store datetime as string for FullCalendar
    booked = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Convert model data to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title if self.booked else "Available Slot",
            'start': self.start,
            'color': '#ff0000' if self.booked else '#008000'  # Red if booked, green if available
        }
