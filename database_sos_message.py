import mysql.connector
import logging
from datetime import datetime, date
import time
import signal
import sys
from tabulate import tabulate

class SOSDatabaseHandler:
    def __init__(self, host='127.0.0.1', database='sos_system', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None
        self.setup_logging()
        self.connect()
        self.last_checked_time = datetime.now()
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
            raise

    def get_all_sos_messages(self):
        try:
            query = "SELECT * FROM button_logs ORDER BY timestamp DESC"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            self.logger.error(f"Error fetching all SOS messages: {e}")
            return []

    def get_new_records(self):
        try:
            query = """
            SELECT * FROM button_logs 
            WHERE timestamp > %s 
            ORDER BY timestamp DESC
            """
            self.cursor.execute(query, (self.last_checked_time,))
            records = self.cursor.fetchall()
            if records:
                self.last_checked_time = records[0]['timestamp']
            return records
        except mysql.connector.Error as e:
            self.logger.error(f"Error fetching new SOS messages: {e}")
            return []

    def get_records_by_date(self, selected_date):
        try:
            query = """
            SELECT * FROM button_logs 
            WHERE DATE(timestamp) = DATE(%s)
            ORDER BY timestamp DESC
            """
            self.cursor.execute(query, (selected_date,))
            records = self.cursor.fetchall()
            print(f"Fetched {len(records)} records for date {selected_date}")
            return records
        except mysql.connector.Error as e:
            self.logger.error(f"Error fetching SOS messages by date: {e}")
            return []

    def run(self):
        print("SOS Database handler started. Press Ctrl+C to stop.")
        print("Displaying all SOS messages:")
        while True:
            try:
                self.refresh_connection()
                all_records = self.get_all_sos_messages()
                if all_records:
                    headers = all_records[0].keys()
                    table_data = [[record[column] for column in headers] for record in all_records]
                    table = tabulate(table_data, headers=headers, tablefmt="grid")
                    print("\nAll SOS messages:")
                    print(table)
                else:
                    print("\nNo SOS messages found in the database.")
                print("\nWaiting for 5 seconds before refreshing...")
                time.sleep(5)  # Wait for 5 seconds before refreshing
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

    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

# Usage example
if __name__ == "__main__":
    db = SOSDatabaseHandler()
    db.run()
