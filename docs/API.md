### Query Natural Language (To Be Implemented)

**POST** `/api/v1/query`

Process natural language queries and return results.

Request:
```json
{
  "query": "Show me average temperature from last hour"
}

Response:

{
  "response": "Query results and insights",
  "data": [...],
  "sql_query": "SELECT AVG(temperature) FROM iot_sensors WHERE time > now() - 1h"
}
