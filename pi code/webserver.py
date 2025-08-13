from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
import datetime

# === Flask App Setup ===
app = Flask(__name__)
auth = HTTPBasicAuth()

# === User Authentication ===
users = {
    "admin": generate_password_hash("raspberry")  # change password if needed
}

@auth.verify_password
def verify(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# === GPIO Setup ===
RED = 14     # GPIO14 (Physical pin 8)
YELLOW = 15  # GPIO15 (Physical pin 10)
GREEN = 18   # GPIO18 (Physical pin 12)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in [RED, YELLOW, GREEN]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# === SQLite Database Setup ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traffic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

with app.app_context():
    db.create_all()

# === Routes ===
@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/set/<color>')
@auth.login_required
def set_color(color):
    color = color.lower()
    GPIO.output(RED, color == 'red')
    GPIO.output(YELLOW, color == 'yellow')
    GPIO.output(GREEN, color == 'green')

    # Save to database
    new_log = LightLog(color=color)
    db.session.add(new_log)
    db.session.commit()

    return f"Set to {color}. <a href='/'>Back</a>"

@app.route('/logs')
@auth.login_required
def logs():
    entries = LightLog.query.order_by(LightLog.timestamp.desc()).limit(20).all()
    return render_template('logs.html', entries=entries)

@app.route('/clear')
@auth.login_required
def clear_logs():
    db.session.query(LightLog).delete()
    db.session.commit()
    return "Logs cleared. <a href='/'>Back</a>"

# === Cleanup on Shutdown ===
@app.route('/off')
@auth.login_required
def shutdown_lights():
    for pin in [RED, YELLOW, GREEN]:
        GPIO.output(pin, GPIO.LOW)
    return "All LEDs off. <a href='/'>Back</a>"

# === Run Server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
