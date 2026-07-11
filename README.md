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
| **Decoupled Architecture** | API and Worker layers communicate strictly asynchronously via Redis |
| **Real-Time Telemetry** | Heartbeat monitoring and comprehensive queue statistics |
| **Forensic Audit Trails** | Complete execution and retry history stored immutably in PostgreSQL |

## Development Methodology

This project follows an **Agile Scrum SDLC** with 11 iterative sprints, prioritizing reliability, scalability, and observability:

| Sprint | Phase | Status |
|--------|-------|--------|
| 0 | Requirements Analysis, Threat Modeling & Architecture | ✅ Complete |
| 1 | High-Level Architecture Diagrams & Trade-offs | ✅ Complete |
| 2 | Database Design & ER Modeling | ✅ Complete |
| 3 | Backend Foundation (FastAPI, DI, Auth) | ✅ Complete |
| 4 | Queue Management (REST APIs, Metrics) | ⏳ In Progress |
| 5 | Job Scheduling (Immediate, Cron, Batch, DLQ) | 🗓️ Planned |
| 6 | Worker Service (Polling, Heartbeat, Recovery) | 🗓️ Planned |
| 7 | Frontend Dashboard (React, Tailwind) | 🗓️ Planned |
| 8 | Monitoring (Logs, Audits, Health) | 🗓️ Planned |
| 9 | Comprehensive Testing Suite | 🗓️ Planned |
| 10 | Final Documentation & Deployment | 🗓️ Planned |

## Architecture Stack

- **Primary Database**: PostgreSQL (Persistent State, Auditing)
- **Queue/Cache**: Redis (Fast IO, Atomic Locks, Sorted Sets)
- **API Gateway**: Python 3.11+ / FastAPI
- **Worker Nodes**: Python 3.11+ / Asyncio / Multiprocessing
- **Frontend UI**: React 18 / Tailwind CSS
- **Infrastructure**: Docker / Kubernetes Ready

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wolfieexd/Distributed-Job-Scheduler.git
cd Distributed-Job-Scheduler

# Start local infrastructure (Redis + Postgres)
docker-compose up -d

# Coming Soon: Run the API and Worker processes
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
