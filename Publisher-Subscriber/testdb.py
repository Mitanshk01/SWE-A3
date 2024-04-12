import sqlite3

DB = "request_booking_db.sqlite"

# Print the entire table
def print_table():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM request_status;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()


# Print venue occupancy table
def print_venue_occupancy():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue_occupancy;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

#print_table()

print_venue_occupancy()