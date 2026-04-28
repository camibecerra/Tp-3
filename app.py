from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class sss(db.Model):
    user_id = db.Column(db.Integer,primary_key = True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String,nullable = True)
    occupation = db.Column(db.String,nullable = True)
    daily_screen_time_hours = db.Column(db.Float)
    phone_usage_before_sleep_minutes = db.Column(db.Integer)
    sleep_duration_hours = db.Column(db.Float)
    sleep_quality_score = db.Column(db.Float)
    stress_level = db.Column(db.Float)
    caffeine_intake_cups = db.Column(db.Integer)
    physical_activity_minutes = db.Column(db.Integer)
    notifications_received_per_day = db.Column(db.Integer)
    mental_fatigue_score = db.Column(db.Float)

def index():
    if request.method == "POST":
        task_content = request.form["age", "gender", "occupation", "daily_scren_time_hours", "phone_usage_before_sleep_minutes", "sleep_duration_hours", "sleep_quality_score", "stress_level", "caffeine_intake_cups", "physical_activity_minutes", "notifications_received_per_day", "mental_fatigue_score"]
        new_sss = sss(content = task_content)
        try:
            db.session.add_all
            db.session.commit()
            return redirect("/")
        except:
            return "there was an error saving your sss"
    else:
        tasks = sss.query.order_by(sss.date_created).all()
        return render_template(tasks = tasks)

if __name__ == "__main__":
    app.run(debug=True)