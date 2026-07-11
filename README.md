# Advanced Distributed Job Scheduling & Execution Platform

## Project Codename: **Titan**

[![Architecture](https://img.shields.io/badge/Architecture-Distributed-green)]()
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)]()
[![State](https://img.shields.io/badge/State-Redis%20%7C%20PostgreSQL-blue)]()
[![License](https://img.shields.io/badge/License-Proprietary-red)]()

---

## Overview

Project Titan is a production-quality, highly scalable distributed job scheduler built from the ground up to orchestrate complex asynchronous workloads. The system provides robust fault tolerance, extreme concurrency, and strict multi-tenancy, resembling enterprise-grade scheduling platforms like Celery, Temporal, or AWS SQS.

## Key Engineering Features

| Feature | Description |
|---|---|
| **Strict Multi-Tenancy** | Complete isolation of workloads at the Organization and Project levels |
| **Atomic Claiming** | Redis Lua scripts guarantee race-condition-free, lockless job claiming |
| **Idempotent Execution** | At-least-once delivery guarantees with safe retry mechanisms |
| **Dynamic Priority Queues** | Sorted Sets implementation for real-time priority weighting and delayed jobs |
| **Configurable Retry Engine** | Natively supports Fixed Delay, Linear Backoff, and Exponential Backoff |
| **Dead Letter Queues (DLQ)** | Automatic isolation of terminally failed jobs to prevent queue blocking |
| **Graceful Worker Shutdown** | Intercepts POSIX signals to safely return in-flight jobs to the queue |
# Distributed Job Scheduler (Titan)

An enterprise-grade, high-performance distributed job execution and scheduling platform designed for massive scale, resiliency, and observability.

Built with an architecture inspired by Celery, Temporal, and BullMQ, this system leverages a Dual-Write pattern (PostgreSQL + Redis) to guarantee zero job loss, sub-millisecond queuing, and flawless worker recovery.

---

## 🚀 Key Features
- **Dual-Write Architecture**: Guarantees consistency. Jobs are atomically written to Postgres and pushed to Redis queues.
- **Role-Based Access Control**: Fully secured with JWT Authentication and SHA-256 hashed API Keys for headless workers.
- **Robust Worker Nodes**: Built-in heartbeat tracking, exponential backoff, dead-letter queues, and automatic stalled-job recovery.
- **Comprehensive Observability**: Structured JSON logging (`structlog`) and a dedicated `JobEvent` audit trail for every state change.
- **DDoS Protection**: Pydantic payload size validation and Strict CORS policies ensure memory preservation.
- **Beautiful Dashboard**: A modern "Obsidian Flux" dark-mode UI built in React + Vite for monitoring cluster health.

---

## 🏛️ High-Level Architecture

```mermaid
flowchart TD
    %% Clients
    Client((Client App))
    Dashboard((React Dashboard))
    
    %% API Gateway
    subgraph API Layer
        FastAPI[FastAPI Gateway\n- JWT/API Key Auth\n- ContextVar Trace ID]
    end
    
    %% Storage & Queues
    subgraph Dual-Write Persistence
        Postgres[(PostgreSQL 15)\n- Source of Truth\n- Audit Logs]
        Redis[(Redis 7.0)\n- Immediate/Delayed Queues\n- Pub/Sub]
    end
    
    %% Workers
    subgraph Execution Layer
        Worker1[Worker Node 1\n- Asyncio\n- Heartbeats]
        Worker2[Worker Node 2\n- Asyncio\n- Heartbeats]
    end

    %% Flow
    Client -- "1. POST /jobs (JSON)" --> FastAPI
    Dashboard -- "GET /metrics" --> FastAPI
    
    FastAPI -- "2a. Save Job & Audit (Atomic)" --> Postgres
    FastAPI -- "2b. Push Payload & Trace ID" --> Redis
    
    Redis -- "3. BLPOP (Pull Job)" --> Worker1
    Redis -- "3. BLPOP (Pull Job)" --> Worker2
    
    Worker1 -- "4. Update Status (Complete/Fail)" --> Postgres
    Worker2 -- "4. Update Status (Complete/Fail)" --> Postgres
    
    %% Styling
    classDef storage fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    classDef compute fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#fff
    classDef client fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#fff
    
    class Postgres,Redis storage
    class FastAPI,Worker1,Worker2 compute
    class Client,Dashboard client
```

---

## 🛠️ Technology Stack
- **Backend**: FastAPI (Python 3.11), SQLAlchemy 2.0 (Async), Pydantic V2
- **Database**: PostgreSQL 15 (Persistent Storage & Audit)
- **Message Broker**: Redis 7.0 (In-Memory Queues & Pub/Sub)
- **Frontend**: React 18, Vite, TailwindCSS (Obsidian Flux theme)
- **Testing**: Pytest, Asyncio, aiosqlite, fakeredis (85% Coverage)

---

## 💻 Local Setup & Deployment

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.11+ (If running locally without Docker)
- Node.js 18+ (For frontend dev)

### 2. Environment Variables
Create a `.env` file in the root directory (or use the defaults provided in `docker-compose.yml`):
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/scheduler
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_super_secret_jwt_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Deploying with Docker Compose (Recommended)
You can spin up the entire cluster (PostgreSQL, Redis, FastAPI Backend, Worker Node) with a single command:
```bash
docker-compose up --build -d
```

### 4. Running the Frontend Dashboard
Navigate to the frontend directory and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
Access the dashboard at `http://localhost:5173`.

---

## 📚 API Documentation
Once the backend is running, FastAPI automatically generates interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

All administrative endpoints (Organizations, Projects, Queues) require an Admin JWT token.

## 🧪 Running the Test Suite
The backend is fully tested using an isolated in-memory stack (SQLite + FakeRedis). No external dependencies are required!
```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests/ -v --cov=app
```

## Project Structure

```
distributed_scheduler/
├── backend/           # FastAPI Application (API Layer)
│   ├── api/           # REST Endpoints
│   ├── core/          # Configuration & Security
│   ├── db/            # SQLAlchemy Models & Migrations
│   ├── schemas/       # Pydantic Validation Models
│   └── services/      # Core Business Logic
├── worker/            # Asynchronous Execution Engine
│   ├── core/          # Worker Lifecycle Management
│   ├── executor/      # Task Execution & Reporting
│   └── heartbeat/     # Telemetry & Health Monitoring
├── frontend/          # React + Tailwind Dashboard
├── docs/              # Architectural Documentation
│   ├── Sprint_0_Requirements_Analysis.md
│   ├── Sprint_1_High_Level_Architecture.md
│   └── ...
├── tests/             # Comprehensive Test Suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Database & API tests
│   └── concurrency/   # Race-condition load tests
└── docker-compose.yml # Local deployment manifest
```

## Engineering Notice

⚠️ **DESIGN PHILOSOPHY**: This system prioritizes **correctness and fault tolerance over raw speed**, though both are highly optimized. We assume network partitions will occur, worker nodes will crash mid-execution, and downstream APIs will fail. The architecture is built to gracefully recover from all these scenarios without human intervention.
