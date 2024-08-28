import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def connect_to_db():
    conn = psycopg2.connect(
        host=config['PostgreSQL']['host'],
        port=config['PostgreSQL']['port'],
        database=config['PostgreSQL']['database'],
        user=config['PostgreSQL']['user'],
        # password=config['PostgreSQL']['password']
    )
    return conn


def get_users(user_id):
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute(f"SELECT * FROM postgres.users WHERE id = {user_id}")
    user = cur.fetchall()
    cur.close()
    connect.close()
    if user:
        print("user is found")
        return user
    else:
        print("user is not found")
        return None


def create_user(user_id, user_name):
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute("INSERT INTO postgres.users (id, name) VALUES (%s, %s)", (user_id, user_name))
    connect.commit()
    cur.close()
    connect.close()
