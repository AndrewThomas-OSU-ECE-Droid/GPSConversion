import sqlite3
import csv
import os

# Function to read GPS data from CSV (including latitude, longitude, and altitude)
def read_gps_data():
    gps_data = []
    with open('GPSData.csv', 'r') as gps_file:
        csv_reader = csv.reader(gps_file)
        next(csv_reader)  # Skip the header if present
        for row in csv_reader:
            garbage, latitude, longitude, altitude = row  # Include altitude
            gps_data.append((float(latitude), float(longitude), float(altitude)))  # Store (latitude, longitude, altitude)
    return gps_data

# Function to read force data from CSV (timestamp, force)
def read_force_data():
    force_data = []
    with open('Weight.csv', 'r') as force_file:
        csv_reader = csv.reader(force_file)
        next(csv_reader)  # Skip the header if present
        for row in csv_reader:
            timestamp, force = row
            force_data.append((timestamp, force))  # Store (timestamp, force)
    return force_data

# Create the database and table structure
def create_database():
    # Remove the existing database file if it exists (this will reset the table)
    if os.path.exists("data_acquisition.db"):
        os.remove("data_acquisition.db")

    # Create the new database and table
    conn = sqlite3.connect("data_acquisition.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        force REAL
    )
    """
    )
    conn.commit()
    conn.close()

# Insert data into the database
def insert_data(gps_data, force_data):
    conn = sqlite3.connect("data_acquisition.db")
    cursor = conn.cursor()

    # Ensure both GPS and force data are of the same length
    min_len = min(len(gps_data), len(force_data))

    for i in range(min_len):  # Insert data row by row
        latitude, longitude, altitude = gps_data[i]  # Include altitude
        timestamp, force = force_data[i]

        cursor.execute(
            """
        INSERT INTO sensor_data (
            timestamp, latitude, longitude, altitude, force
        ) VALUES (?, ?, ?, ?, ?)
        """,
            (timestamp, latitude, longitude, altitude, force),
        )

    conn.commit()
    conn.close()

# Main function
if __name__ == "__main__":
    # Read data from CSV files
    gps_data = read_gps_data()
    force_data = read_force_data()

    # Create database and table (and reset it if needed)
    create_database()

    # Insert data into the database
    insert_data(gps_data, force_data)

    print("Data written to 'data_acquisition.db'")
