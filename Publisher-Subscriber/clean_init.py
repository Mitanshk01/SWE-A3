from utilities import delete_all_tables, create_status_table, \
    create_venue_occupancy_table

if __name__ == "__main__":
    delete_all_tables()
    create_status_table()
    create_venue_occupancy_table()