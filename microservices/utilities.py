import sqlite3

def create_table():
    """
    Create a table to store request statuses if it doesn't exist already.
    """
    conn = sqlite3.connect('request_status_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS request_status (
                          request_id TEXT PRIMARY KEY,
                          status TEXT
                      );''')
    conn.commit()
    conn.close()

def update_status(request_id, status):
    """
    Update the status of a booking request in the SQLite database.

    Parameters:
        request_id (str): The unique identifier of the booking request.
        status (str): The status to be updated for the booking request.
    """
    try:
        conn = sqlite3.connect('request_status_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO request_status (request_id, status)
                        VALUES (?, ?);''', (request_id, status))
        conn.commit()
        conn.close()
    except:
        create_table()
        conn = sqlite3.connect('request_status_db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO request_status (request_id, status)
                        VALUES (?, ?);''', (request_id, status))
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
    conn = sqlite3.connect('request_status_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT status FROM request_status WHERE request_id = ?;''', (request_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Unknown Request ID"
