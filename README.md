# Distributed Job Scheduler

A production-grade, highly scalable Distributed Job Scheduler built from scratch. Designed to handle high-throughput asynchronous workloads, scheduled tasks, and robust retry mechanisms for distributed systems.

## 🚀 Overview

This system acts as a centralized broker for executing asynchronous, scheduled, or batch tasks on behalf of external developers and applications. It is built to maximize reliability, scalability, and observability in a multi-tenant environment.

### Core Features
- **Multi-tenancy**: First-class support for Organizations and Projects.
- **Queue Management**: Multiple prioritized queues with concurrency limits.
- **Job Lifecycle**: Support for Immediate, Delayed, Scheduled, Cron, and Batch jobs.
- **Robust Workers**: Highly concurrent workers with atomic job claiming, graceful shutdown, and heartbeat monitoring.
- **Fault Tolerance**: Automatic Dead Letter Queues (DLQ) and retry policies (Fixed, Linear, Exponential Backoff).
- **Observability**: Execution logs, retry history, worker assignment tracking, and queue throughput metrics.

## 🏗️ Architecture Stack

- **Database (Persistent State)**: PostgreSQL - ensuring strong ACID compliance and relational integrity for tenants.
- **Queue / Fast Storage**: Redis - handling atomic job claiming (via Lua scripts), sorted sets for scheduling, and extreme high-throughput operations.
- **Backend API**: Python (FastAPI) - for high-performance async REST APIs.
- **Worker Service**: Python (Asyncio) - lightweight, highly concurrent worker nodes.
- **Frontend Dashboard**: React + Tailwind CSS - modern interface for queue and job management.
- **Infrastructure**: Docker & Kubernetes - built for containerized, horizontally scalable deployments.

## 🗺️ Project Roadmap (Agile Sprints)

The project is developed iteratively following Agile Scrum methodology:

- [x] **Sprint 0**: Requirements Analysis
- [x] **Sprint 1**: High-Level Architecture
- [ ] **Sprint 2**: Database Design
- [ ] **Sprint 3**: Backend Foundation
- [ ] **Sprint 4**: Queue Management
- [ ] **Sprint 5**: Job Scheduling
- [ ] **Sprint 6**: Worker Service
- [ ] **Sprint 7**: Frontend Dashboard
- [ ] **Sprint 8**: Monitoring
- [ ] **Sprint 9**: Testing
- [ ] **Sprint 10**: Documentation

## 📚 Documentation
Detailed architectural and design documents can be found in the [`docs/`](docs/) directory:
- [Sprint 0: Requirements Analysis](docs/Sprint_0_Requirements_Analysis.md)
- [Sprint 1: High-Level Architecture](docs/Sprint_1_High_Level_Architecture.md)

---
*Built with a focus on engineering quality, correctness, scalability, and production readiness.*
