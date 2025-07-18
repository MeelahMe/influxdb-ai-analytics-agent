from influxdb_client_3 import InfluxDBClient3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Create client
client = InfluxDBClient3(
    host=os.getenv("INFLUXDB_URL", "http://localhost:8181"),
    token=os.getenv("INFLUXDB_TOKEN"),
    org=os.getenv("INFLUXDB_ORG", "myorg")
)

# Write a data point - InfluxDB 3 format
data_point = {
    "measurement": "iot_sensors",
    "tags": {
        "sensor_id": "sensor_001",
        "location": "room_1"
    },
    "fields": {
        "temperature": 22.5,
        "humidity": 45.2,
        "pressure": 1013.25
    },
    "time": datetime.now()
}

try:
    # Write data
    client.write(database="analytics", record=data_point)
    print("Successfully wrote data point!")
    
    # Query data
    query = "SELECT * FROM iot_sensors ORDER BY time DESC LIMIT 5"
    result = client.query(query=query, database="analytics", language="sql")
    
    print("\nQuery results:")
    for row in result:
        print(dict(row))
        
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
