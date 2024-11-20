# Functions connected with database
import sqlite3
import json
from models import Human

DB_NAME = 'selfmosaic.db'

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS human (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            traits TEXT,
            habits TEXT,
            hobbies TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_human(human):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO human (name, age, traits, habits, hobbies)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        human.name,
        human.age,
        json.dumps(human.traits),
        json.dumps(human.habits),
        json.dumps(human.hobbies)
    ))
    conn.commit()
    conn.close()

def get_humans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, age, traits, habits, hobbies FROM human')
    rows = cursor.fetchall()
    humans = []
    for row in rows:
        traits = json.loads(row[2]) if row[2] else {}
        habits = json.loads(row[3]) if row[3] else {}
        hobbies = json.loads(row[4]) if row[4] else []
        human = Human(row[0], row[1], traits, habits, hobbies)
        humans.append(human)
    conn.close()
    return humans

def update_human(name, age, traits, habits, hobbies):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE human
        SET age = ?, traits = ?, habits = ?, hobbies = ?
        WHERE name = ?
    ''', (
        age,
        json.dumps(traits),
        json.dumps(habits),
        json.dumps(hobbies),
        name
    ))
    conn.commit()
    conn.close()

