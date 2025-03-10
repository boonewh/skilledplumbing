from flask_mail import Mail, Message
from app import app, mail

with app.app_context():
    msg = Message("Test Email", sender="boonewh@pathsixdesigns.com", recipients=["boonewh@pathsixdesigns.com"])
    msg.body = "This is a test email from Flask."
    
    try:
        mail.send(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
