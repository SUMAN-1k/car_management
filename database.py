import sqlite3
import os

db_name="car_rental.db"

def connect_db():
    return sqlite3.connect(db_name)

def initialize_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where database.py lives
    schema_path = os.path.join(base_dir, 'schema.sql')      # Absolute path to schema.sql
    
    with open(schema_path, "r") as f:
        sql_script = f.read()
    conn = connect_db()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()