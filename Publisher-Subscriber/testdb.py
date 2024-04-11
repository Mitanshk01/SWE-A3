
from utilities import *


status = get_status_from_db('REQ-1-3')
print(status)

DB_NAME = "request_booking_db.sqlite"

# print the entire table
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('''SELECT * FROM request_status;''')
result = cursor.fetchall()
print(result)
conn.close()
