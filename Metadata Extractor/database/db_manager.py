import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='data.db'):
        """
        Initialize the DatabaseManager with a database connection.

        :param db_name: Name of the SQLite database file.
        """
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_filetable()

    def create_filetable(self):
        """
        Create the 'filestable' if it does not already exist.
        """
        try:
            self.c.execute(
                '''
                CREATE TABLE IF NOT EXISTS filestable (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    filetype TEXT,
                    filesize TEXT,
                    uploadDate TIMESTAMP
                )
                '''
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def add_file_details(self, filename, filetype, filesize, upload_date=None):
        """
        Add a new file's details to the 'filestable'.

        :param filename: Name of the file.
        :param filetype: Type of the file.
        :param filesize: Size of the file.
        :param upload_date: Timestamp of when the file was uploaded. Defaults to current time.
        """
        if upload_date is None:
            upload_date = datetime.now()
        try:
            self.c.execute(
                '''
                INSERT INTO filestable (filename, filetype, filesize, uploadDate)
                VALUES (?, ?, ?, ?)
                ''',
                (filename, filetype, filesize, upload_date)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")

    def view_all_data(self):
        """
        Retrieve all data from the 'filestable'.

        :return: A list of tuples containing all rows in the 'filestable'.
        """
        try:
            self.c.execute('SELECT * FROM filestable')
            data = self.c.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}")
            return []

    def close(self):
        """
        Close the database connection.
        """
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"An error occurred while closing the connection: {e}")
