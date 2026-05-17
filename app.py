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


PROMEDIOS = {
    'daily_screen_time_hours': 5.5,
    'sleep_duration_hours': 6.51,
    'stress_level': 6.98,
    'caffeine_intake_cups': 2.0,
    'physical_activity_minutes': 59.2,
    'notifications_received_per_day': 160.9,
    'mental_fatigue_score': 6.87,
    'sleep_quality_score': 6.25,
}

def calcular_resultado(datos):
    puntaje = 0
    puntaje += min(datos['sleep_quality_score'], 10) * 0.25
    puntaje += min(datos['sleep_duration_hours'] / 9 * 10, 10) * 0.20
    puntaje += max(0, (10 - datos['stress_level'])) * 0.15
    puntaje += max(0, (10 - datos['mental_fatigue_score'])) * 0.10
    puntaje += max(0, (10 - datos['daily_screen_time_hours'])) * 0.10
    puntaje += max(0, (10 - datos['phone_usage_before_sleep_minutes'] / 12)) * 0.08
    puntaje += min(datos['physical_activity_minutes'] / 12, 10) * 0.07
    puntaje += max(0, (10 - datos['caffeine_intake_cups'] * 2.5)) * 0.05
    puntaje = round(min(puntaje, 10), 1)

    if puntaje >= 8:
        label = "Excelente — tu descanso es muy saludable 🌙"
    elif puntaje >= 6:
        label = "Bien — hay algunos aspectos que podés mejorar"
    elif puntaje >= 4:
        label = "Regular — te recomendamos trabajar en tus hábitos"
    else:
        label = "Crítico — tu descanso necesita atención urgente"

    aspectos = []

    if datos['stress_level'] > 7:
        aspectos.append({'titulo': 'Estrés alto', 'descripcion': f'Tu nivel de estrés es {datos["stress_level"]}/10. El promedio es 6.98. Intentá técnicas de relajación antes de dormir.', 'tipo': 'malo'})
    elif datos['stress_level'] > 5:
        aspectos.append({'titulo': 'Estrés moderado', 'descripcion': f'Tu estrés ({datos["stress_level"]}/10) está dentro del promedio pero podría bajar.', 'tipo': 'regular'})

    if datos['daily_screen_time_hours'] > 7:
        aspectos.append({'titulo': 'Demasiada pantalla', 'descripcion': f'Usás {datos["daily_screen_time_hours"]} hs de pantalla por día. El promedio es 5.5 hs. Reducirlo mejoraría tu sueño un ~12%.', 'tipo': 'malo'})
    elif datos['daily_screen_time_hours'] > 5:
        aspectos.append({'titulo': 'Pantalla moderada', 'descripcion': f'Usás {datos["daily_screen_time_hours"]} hs de pantalla, levemente por encima del promedio (5.5 hs).', 'tipo': 'regular'})

    if datos['sleep_duration_hours'] < 6:
        aspectos.append({'titulo': 'Pocas horas de sueño', 'descripcion': f'Dormís {datos["sleep_duration_hours"]} hs por noche. Lo recomendado es 8 hs. El promedio es 6.51 hs.', 'tipo': 'malo'})
    elif datos['sleep_duration_hours'] >= 7.5:
        aspectos.append({'titulo': 'Buenas horas de sueño', 'descripcion': f'Dormís {datos["sleep_duration_hours"]} hs, por encima del promedio (6.51 hs). ¡Muy bien!', 'tipo': 'bueno'})

    if datos['phone_usage_before_sleep_minutes'] > 60:
        aspectos.append({'titulo': 'Celular antes de dormir', 'descripcion': f'Usás el celular {datos["phone_usage_before_sleep_minutes"]} min antes de dormir. Intentá reducirlo a menos de 30 min.', 'tipo': 'malo'})

    if datos['physical_activity_minutes'] < 30:
        aspectos.append({'titulo': 'Poca actividad física', 'descripcion': f'Hacés {datos["physical_activity_minutes"]} min de actividad por día. El promedio es 59 min. Más ejercicio mejora el sueño.', 'tipo': 'malo'})
    elif datos['physical_activity_minutes'] >= 60:
        aspectos.append({'titulo': 'Buena actividad física', 'descripcion': f'Hacés {datos["physical_activity_minutes"]} min de ejercicio por día. ¡Estás por encima del promedio!', 'tipo': 'bueno'})

    if datos['mental_fatigue_score'] > 7:
        aspectos.append({'titulo': 'Fatiga mental alta', 'descripcion': f'Tu fatiga mental es {datos["mental_fatigue_score"]}/10. El promedio es 6.87. Considerá pausas activas durante el día.', 'tipo': 'malo'})

    if datos['caffeine_intake_cups'] >= 3:
        aspectos.append({'titulo': 'Mucha cafeína', 'descripcion': f'Tomás {datos["caffeine_intake_cups"]} cafés por día. El promedio es 2. Evitá el café después de las 14 hs.', 'tipo': 'regular'})

    comparacion = [
        {'label': 'Horas de pantalla', 'tuvalor': f'{datos["daily_screen_time_hours"]} hs', 'promedio': '5.5 hs'},
        {'label': 'Horas dormidas', 'tuvalor': f'{datos["sleep_duration_hours"]} hs', 'promedio': '6.51 hs'},
        {'label': 'Nivel de estrés', 'tuvalor': f'{datos["stress_level"]}/10', 'promedio': '6.98/10'},
        {'label': 'Calidad de sueño', 'tuvalor': f'{datos["sleep_quality_score"]}/10', 'promedio': '6.25/10'},
        {'label': 'Fatiga mental', 'tuvalor': f'{datos["mental_fatigue_score"]}/10', 'promedio': '6.87/10'},
        {'label': 'Actividad física', 'tuvalor': f'{datos["physical_activity_minutes"]} min', 'promedio': '59 min'},
    ]

    return {'puntaje': puntaje, 'label': label, 'aspectos': aspectos, 'comparacion': comparacion}



@app.route("/formulario", methods=['GET', 'POST'])
def formulario():
    resultado = None
    if request.method == 'POST':
        datos = {
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'occupation': request.form['occupation'],
            'daily_screen_time_hours': float(request.form['daily_screen_time_hours']),
            'phone_usage_before_sleep_minutes': int(request.form['phone_usage_before_sleep_minutes']),
            'sleep_duration_hours': float(request.form['sleep_duration_hours']),
            'sleep_quality_score': float(request.form['sleep_quality_score']),
            'stress_level': float(request.form['stress_level']),
            'caffeine_intake_cups': int(request.form['caffeine_intake_cups']),
            'physical_activity_minutes': int(request.form['physical_activity_minutes']),
            'notifications_received_per_day': int(request.form['notifications_received_per_day']),
            'mental_fatigue_score': float(request.form['mental_fatigue_score']),
        }

        # Guardar en la base de datos
        nueva_entrada = sss(
            age=datos['age'],
            gender=datos['gender'],
            occupation=datos['occupation'],
            daily_screen_time_hours=datos['daily_screen_time_hours'],
            phone_usage_before_sleep_minutes=datos['phone_usage_before_sleep_minutes'],
            sleep_duration_hours=datos['sleep_duration_hours'],
            sleep_quality_score=datos['sleep_quality_score'],
            stress_level=datos['stress_level'],
            caffeine_intake_cups=datos['caffeine_intake_cups'],
            physical_activity_minutes=datos['physical_activity_minutes'],
            notifications_received_per_day=datos['notifications_received_per_day'],
            mental_fatigue_score=datos['mental_fatigue_score']
        )
        db.session.add(nueva_entrada)
        db.session.commit()

        resultado = calcular_resultado(datos)

    return render_template("formulario.html", resultado=resultado)



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