# InfluxDB AI Analytics Agent

An intelligent time-series analytics agent that enables natural language querying of InfluxDB 3 data with real-time visualization and AI-powered insights.

**Project Status: In Development**: This project is curerntly being built. Documentation will be updated as features are implemented.

## Features

- **Natural Language Queries**: Ask questions about your time-series data in plain English (for now... would like to expand to multi languages)
- **AI-Powered Analytics**: Automatic pattern detection, anomaly identification, and predictive insights 
- **Real-Time Visualization**: Interactive charts and dashboards with live data updates
- **Conversational Interface**: Chat-based UI with context-aware responses
- **Performance Optimized**: Redis caching, querying optimization, and eefficient data processing 

---

## Prerequisites

- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- InfluxDB 3 Cloud account (or local InfluxDB v2 for development)

--- 

## Setup Instructions

```bash
#Clone the repository
git clone https://github.com/MeelahMe/influxdb-ai-analytics-agent.git
cd influxdb-ai-analytics-agent

# Edit .env with your configuration
cp .env.example .env

# Start backend
cd backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# start frontend (new terminal)
cd frontend
npm install
npm run dev
```
---

## Access Points
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API DOcumentation: `http://localhost:8000/docs`

---

## Documentation

- [Detailed Setup Guide](docs/SETUP.md) - Comprehensive installation instructions 
- Architecture - System design and components (coming soon)
- API Reference - Endpoint documentation (coming soon)

---

## Tech Stack

**Backend**

- FastAPI - Modern Python web framework 
- InfluxDB 3 - Time-series database
- WebSockets - Real-time communication

**Frontend**

- React 18 with TypeScript
- Vite - Build tool and dev server
- Tailwind CSS - Utility-first styling
- Recharts - Data visualization 

---

Built with ❤️ for the time-series analytics community