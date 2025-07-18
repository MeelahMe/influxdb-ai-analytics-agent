# Detailed Setup Guide

This guide provides comprehensive setup instructions for the InfluxDB AI Analytics Agent.
Table of Contents

---

## Prerequisites

- Environment Setup
- Backend Setup
- Frontend Setup
- Database Setup
- Running the Application
- Troubleshooting

---

## Prerequisites

Ensure you have the following installed:

- Python 3.9+
```bash
bashpython --version  # Should show 3.9 or higher
```

- Node.js 16+ and npm
```bash
bashnode --version  # Should show v16 or higher
npm --version
```

- Git
```bash
bashgit --version
```

- Docker & Docker Compose (optional but recommended)
```bash
bashdocker --version
docker-compose --version
```

---

## Environment Setup

1. Clone the repository
```bash
bashgit clone https://github.com/MeelahMe/influxdb-ai-analytics-agent.git
cd influxdb-ai-analytics-agent
```

2. Create environment configuration
```bash
bashcp .env.example .env
```

3. Configure environment variables
```bash
Edit .env file with your settings:
bash# InfluxDB Configuration
INFLUXDB_URL=http://localhost:8086  # For local development
INFLUXDB_TOKEN=your-token-here
INFLUXDB_ORG=your-org
INFLUXDB_BUCKET=analytics

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Application Settings
APP_SECRET_KEY=generate-a-secret-key
FRONTEND_URL=http://localhost:5173
```

---

## Backend Setup

**Option 1**: Manual Setup

1. Navigate to backend directory
```bash
bashcd backend
```

2. Create virtual environment
```bash
bashpython -m venv venv
```

3. Activate virtual environment

- Linux/macOS:
```bash
bashsource venv/bin/activate
```

- Windows:
```bash
bashvenv\Scripts\activate
```

4. Install dependencies
```bash
bashpip install -r requirements.txt
```

5. un the backend server
```bash
bashuvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Verify backend is running
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Option 2**: Docker Setup

```bash
docker-compose up backend
```

--- 

## Frontend Setup

**Option 1**: Manual Setup

1. Navigate to frontend directory
```bash
cd frontend 
```

2. Install dependencies
```bash
npm install
``` 

3. Start development server
```bash
npm run dev
```

4. Access frontend
- Development server: `http://localhost:5173`

**Option 2**: Docker Setup

```bash
docker-compose up fronted
```

# Database Setup

**Option 1**: Local InfluxDB (Development)

1. Using Docker
```bash
docker run -d \
  --name influxdb-local \
  -p 8086:8086 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=adminpassword \
  -e DOCKER_INFLUXDB_INIT_ORG=myorg \
  -e DOCKER_INFLUXDB_INIT_BUCKET=analytics \
  -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=mytoken \
  influxdb:2.7
```

2. Access InfluxDB UI
- URL: `http://localhost:8086`
- Username: adim
- Password: adminpassword

**Option 3**: InfluxDb 3 Core (Recommended- Latest Version)

1. Install InfluxDB 3 Core
```bash
curl -O https://www.influxdata.com/d/install_influxdb3.sh \
  && sh install_influxdb3.sh
```

2. Start InfluxDB 3 Core
```bash
influxdb3 serve \
  --node-id host01 \
  --object-store file \
  --data-dir ~/.influxdb3
```

3. Create the analytics database
```bash
influxdb3 create token --admin
# Save the token securely
```

4. Create the analytics database
```bash
influxdb3 create database analytics \
  --token "your-admin-token" \
  --host "http://localhost:8181"
```

5. Update .env with InfluxDB 3 settings
```bash
INFLUXDB_URL=http://localhost:8181
INFLUXDB_TOKEN=your-admin-token
INFLUXDB_DATABASE=analytics
USE_MOCK_DATA=false
```

---

# Running the Application

## Development Mode (Recommended for initial setup)

1. Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

2. Terminal - Frontend
```bash
cd frontend
npm run dev
```

## Production Mode with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Verifying Your Setup

1. Test InfluxDB 3 Core Connection
```bash
cd backend
python test_influxdb3_write.py
```

2. Test API Endpoints
```bash
# Start the backend server
uvicorn app.main:app --reload
```

# In another terminal, test endpoints
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/test-connection
```

3. Access API Documentation

- Open http://localhost:8000/docs for Swagger UI
- Open http://localhost:8000/redoc for ReDoc