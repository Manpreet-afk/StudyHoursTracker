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

def get_study_time(period="all"):
    conn = get_connection()
    cursor = conn.cursor()

    if period == "today":
        query= "SELECT SUM(minutes) FROM study_sessions WHERE log_date = CURRENT_DATE"
    elif period == "week":
        query= "SELECT SUM(minutes) FROM study_sessions WHERE log_date >= CURRENT_DATE-7"
    elif period == "month":
        query= "SELECT SUM(minutes) FROM study_sessions WHERE log_date >= CURRENT_DATE-30"
    else:
        query= "SELECT SUM(minutes) FROM study_sessions"


    cursor.execute(query)
    result= cursor.fetchone()
    cursor.close()
    conn.close()
    if result[0] is not None:
        return result[0]
    else:
        return 0
    
def update_session(session_id, new_minutes):
    conn= get_connection()
    cursor=conn.cursor()

    try:
        cursor.execute("UPDATE study_sessions SET minutes = %s WHERE id = %s", (new_minutes, session_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating session: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_session(session_id):
    pass
    conn = get_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("DELETE FROM study_sessions WHERE id=%s",(session_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting session: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
        