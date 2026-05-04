from app import app,db ,sss
import pandas as pd

with app.app_context():

    db.create_all()
    print('Se creo la base de datos')

    try:

        df = pd.read_csv('sss.csv')


        if sss.query.first() is None:
            for index, row in df.iterrows():
                record = sss(
                    user_id=row['user_id'],
                    age=row['age'],
                    gender=row['gender'],
                    occupation=row['occupation'],
                    daily_screen_time_hours=row['daily_screen_time_hours'],
                    phone_usage_before_sleep_minutes=row['phone_usage_before_sleep_minutes'],
                    sleep_duration_hours=row['sleep_duration_hours'],
                    sleep_quality_score=row['sleep_quality_score'],
                    stress_level=row['stress_level'],
                    caffeine_intake_cups=row['caffeine_intake_cups'],
                    physical_activity_minutes=row['physical_activity_minutes'],
                    notifications_received_per_day=row['notifications_received_per_day'],
                    mental_fatigue_score=row['mental_fatigue_score']
                )
                db.session.add(record)

            db.session.commit() 
            print(f'Se cargaron {len(df)} registros desde sss.csv')
        else:
            print('La base de datos ya contiene datos')
    except Exception as e:
        print(f'Error al cargar CSV: {e}')