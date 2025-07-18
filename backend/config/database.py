"""
InfluxDB 3 Core Configuration and Connection Management
"""
import os
from typing import Optional, List, Dict, Any
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class InfluxDBConfig:
    """Configuration for InfluxDB 3 Core connection"""
    
    def __init__(self):
        self.url = os.getenv("INFLUXDB_URL", "http://localhost:8181")
        self.token = os.getenv("INFLUXDB_TOKEN")
        self.org = os.getenv("INFLUXDB_ORG", "myorg")
        self.database = os.getenv("INFLUXDB_DATABASE", "analytics")  # InfluxDB 3 uses 'database' instead of 'bucket'
        
        if not self.token:
            raise ValueError("INFLUXDB_TOKEN environment variable is required")


class InfluxDBConnection:
    """Manages InfluxDB 3 Core connection and operations"""
    
    def __init__(self):
        self.use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        if not self.use_mock:
            self.config = InfluxDBConfig()
        self._client: Optional[InfluxDBClient3] = None
        self.mock_data = []  # Store mock data in memory
    
    def get_client(self) -> InfluxDBClient3:
        """Get or create InfluxDB client"""
        if self.use_mock:
            logger.info("Using mock data mode")
            return None
            
        if not self._client:
            self._client = InfluxDBClient3(
                host=self.config.url,
                token=self.config.token,
                org=self.config.org,
                database=self.config.database
            )
            logger.info("InfluxDB 3 Core client initialized successfully")
        return self._client
    
    def write_point(self, measurement: str, tags: dict, fields: dict, timestamp=None):
        """Write a single data point to InfluxDB"""
        if self.use_mock:
            # Store in mock data
            point_data = {
                "measurement": measurement,
                "tags": tags,
                "fields": fields,
                "timestamp": timestamp or datetime.now()
            }
            self.mock_data.append(point_data)
            return
            
        try:
            client = self.get_client()
            
            # Create point with InfluxDB 3 syntax
            point_data = {
                "measurement": measurement,
                "tags": tags,
                "fields": fields
            }
            
            if timestamp:
                point_data["time"] = timestamp
            
            # Write to database
            client.write(
                database=self.config.database,
                record=point_data
            )
            logger.info(f"Successfully wrote point to measurement: {measurement}")
            
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {str(e)}")
            raise
    
    def query(self, query_string: str) -> List[Dict[str, Any]]:
        """Execute a query against InfluxDB"""
        if self.use_mock:
            # Return mock data
            from app.services.agent_service import AgentService
            agent = AgentService()
            return agent._generate_mock_data("iot_sensors")
            
        try:
            client = self.get_client()
            
            # InfluxDB 3 uses SQL syntax
            result = client.query(
                query=query_string,
                database=self.config.database,
                language="sql"  # InfluxDB 3 uses SQL
            )
            
            # Convert to list of dictionaries
            data = []
            for row in result:
                data.append(dict(row))
            
            return data
            
        except Exception as e:
            logger.error(f"Error querying InfluxDB: {str(e)}")
            raise
    
    def create_database(self):
        """Create database if it doesn't exist"""
        if self.use_mock:
            return
            
        try:
            client = self.get_client()
            # In InfluxDB 3, databases are created automatically on first write
            logger.info(f"Database '{self.config.database}' will be created on first write")
        except Exception as e:
            logger.error(f"Error with database setup: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """Test the connection to InfluxDB"""
        if self.use_mock:
            return True
            
        try:
            client = self.get_client()
            # Try a simple query to test connection
            client.query(
                query="SELECT 1",
                database=self.config.database,
                language="sql"
            )
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def close(self):
        """Close the InfluxDB connection"""
        if self._client:
            self._client.close()
            logger.info("InfluxDB connection closed")


# Import datetime for mock data
from datetime import datetime

# Global connection instance
influxdb_conn = InfluxDBConnection()
