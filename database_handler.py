import mysql.connector
import logging
from datetime import datetime, date
import time
import signal
import sys
from tabulate import tabulate
import sqlite3
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class DatabaseHandler:
    def __init__(self, host='127.0.0.1', database='rfidattendance', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None
        self.setup_logging()
        self.connect()
        self.last_id = 0
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor(dictionary=True)
            self.logger.info(f"Connected to database: {self.database}")
        except mysql.connector.Error as e:
            self.logger.error(f"Error connecting to database: {e}")

    def get_user_by_card_uid(self, card_uid):
        try:
            query = "SELECT * FROM users_logs WHERE card_uid = %s ORDER BY checkindate DESC, timein DESC LIMIT 1"
            self.cursor.execute(query, (card_uid,))
            user = self.cursor.fetchone()
            if user:
                return user
            else:
                self.logger.warning(f"No user found with Card UID: {card_uid}")
                return None
        except mysql.connector.Error as e:
            self.logger.error(f"Error fetching user: {e}")
            return None

    def log_attendance(self, person_id, timestamp):
        try:
            query = """
            INSERT INTO users_logs 
            (username, serialnumber, card_uid, device_uid, device_dep, checkindate, timein, timeout, card_out) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, '00:00:00', 0)
            """
            values = (person_id, person_id, person_id, person_id, person_id, 
                      timestamp.date(), timestamp.strftime('%H:%M:%S'))
            self.cursor.execute(query, values)
            self.conn.commit()
            self.logger.info(f"Attendance logged for user: {person_id}")
            return True
        except mysql.connector.Error as e:
            self.logger.error(f"Error logging attendance: {e}")
            return False

    def get_all_records(self):
        try:
            query = "SELECT * FROM users_logs ORDER BY checkindate DESC, timein DESC"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            self.logger.error(f"Error fetching records: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

    def get_new_records(self):
        try:
            query = f"SELECT * FROM users_logs WHERE id > {self.last_id} ORDER BY id ASC"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            if records:
                self.last_id = records[-1]['id']
            return records
        except mysql.connector.Error as e:
            print(f"Error fetching new records: {e}")
            return []

    def run(self):
        print("Database handler started. Press Ctrl+C to stop.")
        print("Waiting for new entries...")
        while True:
            try:
                self.refresh_connection()
                new_records = self.get_new_records()
                if new_records:
                    headers = new_records[0].keys()
                    table_data = [[record[column] for column in headers] for record in new_records]
                    table = tabulate(table_data, headers=headers, tablefmt="grid")
                    print("\nNew entries:")
                    print(table)
                    print("\nWaiting for new entries...")
                time.sleep(1)  # Wait for 1 second before the next check
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(5)  # Wait for 5 seconds before trying again

    def refresh_connection(self):
        if not self.conn or not self.conn.is_connected():
            print("Refreshing database connection")
            self.connect()

    def signal_handler(self, signum, frame):
        print("Received signal to stop. Closing database connection...")
        self.close()
        sys.exit(0)

    def get_records_by_date(self, date):
        try:
            query = "SELECT * FROM users_logs WHERE checkindate = %s ORDER BY timein ASC"
            self.cursor.execute(query, (date,))
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            print(f"Error fetching records by date: {e}")
            return []

    def get_unique_attendance_count(self, date):
        try:
            self.cursor.execute("""
                SELECT COUNT(DISTINCT name) as unique_count, COUNT(*) as total_count
                FROM attendance
                WHERE DATE(timestamp) = %s%s%s
            """, (date,))
            result = self.cursor.fetchone()
            return result['unique_count'], result['total_count']
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0, 0

    def get_unique_attendees_today(self):
        today = date.today()
        query = """
        SELECT COUNT(DISTINCT person_id) 
        FROM attendance 
        WHERE DATE(timestamp) = ?
        """
        self.cursor.execute(query, (today,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance
        (id INTEGER PRIMARY KEY, name TEXT, timestamp DATETIME)
        ''')
        self.conn.commit()

    def log_attendance(self, name, timestamp):
        self.cursor.execute('INSERT INTO attendance (name, timestamp) VALUES (?, ?)',
                            (name, timestamp))
        self.conn.commit()

    def get_attendance_records_by_date(self, date):
        self.cursor.execute('''
        SELECT DISTINCT username,checkindate FROM users_logs where checkindate=%s
                            ''', (date,))

        return self.cursor.fetchall()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.                     
# Usage example
if __name__ == "__main__":
    db = DatabaseHandler()
    db.run()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.