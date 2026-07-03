import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn=psycopg2.connect(
        host="localhost",
        database="studytrackerapp",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    )
    return conn

if __name__ == "__main__":
    try:
        test_conn = get_connection()
        print("Connection successful!")
        test_conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id SERIAL PRIMARY KEY,
            subject TEXT,
            minutes INT,
            log_date DATE
        )
    """)
    
    # 3. Save and close
    conn.commit()
    cursor.close()
    conn.close()