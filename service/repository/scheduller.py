import psycopg2
from service.config import PostgreSQLConfig
from datetime import datetime

def connect_to_db():
    conn = psycopg2.connect(
        host=PostgreSQLConfig.HOST,
        port=PostgreSQLConfig.PORT,
        database=PostgreSQLConfig.DATABASE,
        user=PostgreSQLConfig.USER,
    )
    return conn

def get_schedule(user_id):
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute(f"SELECT * FROM postgres.scheduller WHERE user_id = {user_id} AND is_active = true")
    user = cur.fetchall()
    cur.close()
    connect.close()
    if user:
        print("Schedule date is found")
        return user
    else:
        print("Schedule date is not found")
        return None

def set_schedule(user_id):
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("UPDATE postgres.scheduller SET is_active = false WHERE user_id =(%s)", (user_id))
    cur.execute("INSERT INTO postgres.scheduller (user_id, schedulled_at) VALUES (%s, %s)", (user_id, datetime.now(tz=None).strftime('')))
    connect.commit()
    cur.close()
    connect.close()