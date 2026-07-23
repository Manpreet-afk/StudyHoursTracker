import psycopg2
import os
import datetime
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

def add_session(subject, minutes):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today()
    
    try:
        cursor.execute(
            "INSERT INTO study_sessions (subject, minutes, log_date) VALUES (%s, %s, %s)",
            (subject, minutes, today)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding session: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


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


def get_streak():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT DATE(log_date) FROM study_sessions ORDER BY DATE(log_date) DESC")
    dates = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    if not dates:
        return 0

    streak = 0
    today = datetime.date.today()

    if dates[0] != today and dates[0] != today - datetime.timedelta(days=1):
        return 0

    expected_date = dates[0]
    for d in dates:
        if d == expected_date:
            streak += 1
            expected_date -= datetime.timedelta(days=1)
        else:
            break
            
    return streak


def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, log_date, subject, minutes FROM study_sessions ORDER BY log_date DESC, id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_subject_breakdown():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subject, SUM(minutes) FROM study_sessions GROUP BY subject")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    # Returns a dictionary like {"Python": 120, "SQL": 60}
    return {row[0]: row[1] for row in data}