from datetime import date
from db import get_connection, create_table

def add_session():

    print("Add a new study session ")
    subject = input("what subject did you study? ")

    while True:
        try:
            minutes = int(input("How many minutes? "))
            break
        except ValueError:
            print("Please enter a valid number for minutes.")

    today = date.today()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO study_sessions (subject, minutes, log_date) VALUES (%s, %s, %s)",
            (subject, minutes, today)
        )
        conn.commit()
        print(f"\n Success! Addeed {minutes} minutes of {subject} on {today}.")

    except Exception as e:
        print(f"Error adding session: {e} ")

    finally:
        cursor.close()
        conn.close()


def view_sessions():
    print("\n --All Study Sessions--")
    conn=get_connection()
    cursor=conn.cursor()

    try:
        cursor.execute("SELECT * FROM study_sessions")
        rows=cursor.fetchall()

        if not rows:
            print("No sessions logged yet.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Subject: {row[1]}, Minutes: {row[2]}, Date: {row[3]}")
        
    except Exception as e:
        print(f"Error retrieving sessions: {e}")

    finally:
        cursor.close()
        conn.close()


def main():
    create_table()  
    
    while True:
        print("\n-- Study Tracker --")
        print("1. Log a new session")
        print("2. View all sessions")
        print("3. Quit")

        choice = input("Choose an option: ")
        
        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions() 
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()