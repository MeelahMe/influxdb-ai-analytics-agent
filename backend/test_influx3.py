from influxdb_client_3 import InfluxDBClient3
import os
from dotenv import load_dotenv

load_dotenv()

# Test connection
try:
    client = InfluxDBClient3(
        host=os.getenv("INFLUXDB_URL", "http://localhost:8181"),
        token=os.getenv("INFLUXDB_TOKEN"),
        org=os.getenv("INFLUXDB_ORG", "myorg")
    )
    print("Client created successfully!")
    
    # Try a simple query
    result = client.query(query="SELECT 1", database="analytics", language="sql")
    print("Query successful!")
    
except Exception as e:
    print(f"Error: {e}")
