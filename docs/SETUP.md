# Detailed Setup Guide

This guide provides comprehensive setup instructions for the InfluxDB AI Analytics Agent.
Table of Contents

## Prerequisites

- Environment Setup
- Backend Setup
- Frontend Setup
- Database Setup
- Running the Application
- Troubleshooting

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


## Backend Setup

Option 1: Manual Setup

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