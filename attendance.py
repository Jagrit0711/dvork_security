from database_handler import DatabaseHandler
from datetime import date, datetime
import time

class AttendanceProcessor:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        print("AttendanceProcessor initialized successfully")

    def get_unique_attendees_count(self):
        try:
            today = date.today()
            records = self.db_handler.get_attendance_records_by_date(today)
            unique_names = set()
            for record in records:  
                unique_names.add(record['username'])
            
            unique_count = len(unique_names)
            print(f"Date: {today}")
            print(f"Total records: {len(records)}")
            print(f"Unique attendees today: {unique_count}")
            print(f"Unique names: {', '.join(unique_names)}")
            return unique_count
        except Exception as e:
            print(f"Error in get_unique_attendees_count: {e}")
            return 0
        
# Main loop
if __name__ == "__main__":

    processor = AttendanceProcessor()
    
    try:
        while True:
            unique_count = processor.get_unique_attendees_count()
            print(f"Current unique attendee count: {unique_count}")
            print("--------------------")
            time.sleep(5)  # Wait for 5 seconds before checking again
    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
