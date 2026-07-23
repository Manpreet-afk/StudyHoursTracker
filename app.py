from datetime import date
from db import get_connection, create_table, get_study_time, update_session, delete_session,add_session




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
        print("3. View progress")
        print("4. Edit a session's time")    
        print("5. Delete a session")         
        print("6. Quit")

        choice = input("Choose an option: ")
        
        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3" :
            print("\n-- Select Timeframe --")
            print("1. Today")
            print("2. This Week (Last 7 Days)")
            print("3. This Month (Last 30 Days)")
            print("4. All Time")

            sub_choice = input("Choose a timeframe (1-4): ")

            if sub_choice == '1':
                minutes = get_study_time("today")
                label = "Today's"
            elif sub_choice == '2':
                minutes = get_study_time("week")
                label = "This Week's"
            elif sub_choice == '3':
                minutes = get_study_time("month")
                label = "This Month's"
            elif sub_choice == '4':
                minutes = get_study_time("all")
                label = "All-Time"
            else:
                print("Invalid choice. Returning to main menu.")
                continue

            print(f"Progress: {minutes/60} hours OR {minutes} minutes!")

        elif choice=="4":
            try:
                print("\nTip: Check option 2 (View all sessions) if you forgot your session ID.")
                target_id = int(input("Enter the Session ID you want to edit: "))
                new_mins = int(input("Enter the new study duration (in minutes): "))
                
                if update_session(target_id, new_mins):
                    print(f"Session #{target_id} updated successfully!")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")

        elif choice =="5":
            try:
                target_id = int(input("Enter the Session ID you want to permanently DELETE: "))
                confirm = input(f"Are you sure you want to delete Session #{target_id}? (y/n): ")
                
                if confirm.lower() == 'y':
                    if delete_session(target_id):
                        print(f"Session #{target_id} has been deleted.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid input. Please enter a valid ID number.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()