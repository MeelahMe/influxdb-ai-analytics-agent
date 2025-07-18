"""
Test script for InfluxDB 3 Core write operations
"""
from influxdb_client_3 import InfluxDBClient3, Point
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Create client
client = InfluxDBClient3(
    host=os.getenv("INFLUXDB_URL", "http://localhost:8181"),
    token=os.getenv("INFLUXDB_TOKEN"),
    database="analytics"
)

try:
    # Method 1: Using Point class (recommended)
    print("Writing data using Point class...")
    point = (
        Point("iot_sensors")
        .tag("sensor_id", "sensor_001")
        .tag("location", "room_1")
        .field("temperature", 22.5)
        .field("humidity", 45.2)
        .field("pressure", 1013.25)
        .time(datetime.now())
    )
    
    client.write(database="analytics", record=point)
    print("Successfully wrote data point!")
    
    # Method 2: Using proper dictionary format
    print("\nWriting data using dictionary format...")
    data_dict = {
        "measurement": "iot_sensors",
        "tags": {
            "sensor_id": "sensor_002",
            "location": "room_2"
        },
        "fields": {
            "temperature": 23.1,
            "humidity": 46.8,
            "pressure": 1014.5
        },
        "time": datetime.now()
    }
    
    client.write(database="analytics", record=data_dict)
    print("Successfully wrote dictionary data!")
    
    # Query data
    print("\nQuerying data...")
    query = """
    SELECT * 
    FROM iot_sensors 
    WHERE time >= now() - INTERVAL '1 hour'
    ORDER BY time DESC
    LIMIT 5
    """
    
    result = client.query(query=query, database="analytics", language="sql")
    
    print("\nQuery results:")
    count = 0
    for row in result:
        print(f"Row {count + 1}: {dict(row)}")
        count += 1
    print(f"\nTotal rows retrieved: {count}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()

print("\nInfluxDB 3 Core is working correctly!")
