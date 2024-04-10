import sqlite3

DB_NAME = 'request_booking_db.sqlite'

def create_status_table():
    """
    Create a table to store request statuses if it doesn't exist already.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS request_status (
                          request_id TEXT PRIMARY KEY,
                          venueId INTEGER,
                          seats INTEGER,
                          status TEXT
                      );''')
    conn.commit()
    conn.close()

def start_processing_request(request_data):
    """
    Start processing a booking request by inserting it into the database.

    Parameters:
        request_data (dict): A dictionary containing the parameters:
                             - venueId (int): The ID of the venue.
                             - seats (int): The number of seats requested.
                             - request_id (str): The unique identifier of the booking request.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO request_status (request_id, venueId, seats, status)
                        VALUES (?, ?, ?, ?);''', (request_data['request_id'], request_data['venueId'], request_data['seats'], 'Pending'))
        conn.commit()
        conn.close()
    except:
        create_status_table()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO request_status (request_id, venueId, seats, status)
                        VALUES (?, ?, ?, ?);''', (request_data['request_id'], request_data['venueId'], request_data['seats'], 'Pending'))
        conn.commit()
        conn.close()

def update_request_status(request_id, status):
    """
    Update the status of a booking request in the SQLite database.

    Parameters:
        request_id (str): The unique identifier of the booking request.
        status (str): The status to be updated for the booking request.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''UPDATE request_status SET status = ? WHERE request_id = ?;''', (status, request_id))
    conn.commit()
    conn.close()

def get_status_from_db(request_id):
    """
    Retrieve the status of a booking request from the SQLite database.

    Parameters:
        request_id (str): The unique identifier of the booking request.

    Returns:
        str: The status of the booking request.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT status FROM request_status WHERE request_id = ?;''', (request_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Unknown Request ID"

def delete_all_tables():
    """
    Delete all tables in the request_status_db.sqlite database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE {table[0]};")
    conn.commit()
    conn.close()
