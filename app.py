from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd



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

def generar_grafico_lineal(x_value, y_value):


    lista = sss.query.all()
    filtered_list = []

    grupos = {}

    for item in lista:
        if getattr(item, x_value) is not None and getattr(item, y_value) is not None:
          filtered_list.append(item)



    for item in lista:
        x = getattr(item, x_value)
        y = getattr(item, y_value)

        if x is not None and y is not None:
            if x not in grupos:
                grupos[x] = []
            grupos[x].append(y)

    x_vals = []
    y_promedios = []

    for x in sorted(grupos):
        promedio = sum(grupos[x]) / len(grupos[x])
        x_vals.append(x)
        y_promedios.append(promedio)



    plt.figure(figsize=(10,5))
    plt.plot(x_vals, y_promedios)
    plt.xlabel(x_value)
    plt.ylabel(y_value)
    plt.title(f"{y_value} vs {x_value}")

    plt.savefig(f"static/plots/{f'{y_value} vs {x_value}'}.png")
    plt.close()

    return  

def generar_grafico_barra(x_value, y_value):


    lista = sss.query.all()
    filtered_list = []

    grupos = {}

    for item in lista:
        if getattr(item, x_value) is not None and getattr(item, y_value) is not None:
          filtered_list.append(item)



    for item in lista:
        x = getattr(item, x_value)
        y = getattr(item, y_value)

        if x is not None and y is not None:
            if x not in grupos:
                grupos[x] = []
            grupos[x].append(y)

    x_vals = []
    y_promedios = []

    for x in sorted(grupos):
        promedio = sum(grupos[x]) / len(grupos[x])
        x_vals.append(x)
        y_promedios.append(promedio)



    plt.figure(figsize=(10,5))
    plt.bar(x_vals, y_promedios)
    plt.xlabel(x_value)
    plt.ylabel(y_value)
    plt.title(f"{y_value} vs {x_value}")

    plt.savefig(f"static/plots/{f'{y_value} vs {x_value}'}.png")
    plt.close()

    return  


"""
@app.route("/plots")
def graph():
    generar_grafico_lineal("age", "sleep_duration_hours")
    generar_grafico_lineal("age", "daily_screen_time_hours")
    generar_grafico_lineal("age", "stress_level")

    generar_grafico_lineal("occupation", "daily_screen_time_hours")
    generar_grafico_lineal("occupation", "sleep_duration_hours")
    generar_grafico_lineal("occupation", "stress_level")
    generar_grafico_lineal("occupation", "sleep_quality_score")
    
    generar_grafico_lineal("daily_screen_time_hours", "mental_fatigue_score")
    generar_grafico_lineal("daily_screen_time_hours", "sleep_quality_score")
    
    generar_grafico_lineal("stress_level", "sleep_quality_score")
    generar_grafico_lineal("stress_level", "sleep_duration_hours")
    generar_grafico_lineal("stress_level", "mental_fatigue_score")
    
    generar_grafico_lineal("sleep_quality_score", "sleep_duration_hours")
    generar_grafico_lineal("caffeine_intake_cups", "sleep_duration_hours")
    
    generar_grafico_lineal("phone_usage_before_sleep_minutes", "sleep_quality_score")
    generar_grafico_lineal("mental_fatigue_score", "sleep_quality_score")
    

    return ""


"""
















@app.route("/formulario")
def formulario():
    return render_template("formulario.html")




@app.route("/predicciones")
def predicciones():
    return render_template("predicciones.html")


@app.route("/graficos")
def graficos():

    generar_grafico_lineal("age", "sleep_duration_hours")
    generar_grafico_lineal("age", "daily_screen_time_hours")
    generar_grafico_lineal("age", "stress_level")

    generar_grafico_lineal("occupation", "daily_screen_time_hours")
    generar_grafico_lineal("occupation", "sleep_duration_hours")
    generar_grafico_lineal("occupation", "stress_level")
    generar_grafico_lineal("occupation", "sleep_quality_score")
    
    generar_grafico_lineal("daily_screen_time_hours", "mental_fatigue_score")
    generar_grafico_lineal("daily_screen_time_hours", "sleep_quality_score")
    
    generar_grafico_lineal("stress_level", "sleep_quality_score")
    generar_grafico_lineal("stress_level", "sleep_duration_hours")
    generar_grafico_lineal("stress_level", "mental_fatigue_score")
    
    generar_grafico_lineal("sleep_quality_score", "sleep_duration_hours")
    generar_grafico_lineal("caffeine_intake_cups", "sleep_duration_hours")
    
    generar_grafico_lineal("phone_usage_before_sleep_minutes", "sleep_quality_score")
    generar_grafico_lineal("mental_fatigue_score", "sleep_quality_score")

    
    return render_template("graficos.html")

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__ == "__main__":

    app.run(debug=True)