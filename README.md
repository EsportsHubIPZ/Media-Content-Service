<div align="center">

# Media & Content Service

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-FF6600.svg?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean%2FDDD-2ea44f?style=for-the-badge)](#)

*A highly scalable, decoupled microservice engineered to manage the ingress, validation, persistence, and distribution of media assets and platform-wide news.*

</div>

---

> **Architectural Maxim:** *"Isolate the domain. Defer infrastructural decisions. Guarantee transactional integrity."*

The **Media & Content Service** is a Tier-1 bounded context within the Esports Hub distributed system. It provides an authoritative source of truth for binary assets (match evidence, avatars) and content syndication (news feeds). Engineered around the principles of **Domain-Driven Design (DDD)** and **Clean Architecture**, this service is heavily decoupled, ensuring horizontal scalability and robust fault tolerance.

---

<details open>
<summary><b>Interactive Table of Contents</b></summary>

1. [System Architecture (C4 Model)](#1-system-architecture)
2. [Domain Data Model (ERD)](#2-domain-data-model)
3. [API Specifications](#3-api-specifications)
   - [Synchronous (REST)](#synchronous-rest-contracts)
   - [Asynchronous (AMQP)](#asynchronous-amqp-contracts)
4. [Infrastructure & Configuration](#4-infrastructure--configuration)
5. [Project Structure](#5-project-structure)

</details>

---

## 1. System Architecture

The core topology of the Media & Content Service relies on a strict separation of concerns. It operates behind an API Gateway, functioning as a standalone node that interacts with its own dedicated infrastructure.

![C4 Component Architecture](docs/c4.png)

As demonstrated in the **C4 Component Diagram** above:
* **Ingress:** All external traffic (from Users or Admins) routes strictly through the central **API Gateway**, which offloads JWT authentication before passing requests to our FastAPI Controllers.
* **Storage Abstraction:** The `Storage Service` acts as the coordinator for heavy binary streams. It validates constraints locally, streams binaries to **Object Storage (MinIO / S3)**, and only upon success, commits a reference to the **PostgreSQL** metadata database.
* **Asynchronous Publishing:** The `News Service` leverages an event-driven pattern. Upon successful state mutations (e.g., publishing a news article), it hands off a domain event to the `Message Publisher`, which routes the payload into **RabbitMQ**.

> [!NOTE]
> **Design Decision:** Binary objects are never stored in PostgreSQL. The database stores strictly typed metadata with a referencing `s3_key`, effectively decoupling the storage tier from the application state tier.

---

## 2. Domain Data Model

To ensure transactional integrity and complex querying capabilities, the service utilizes a normalized relational schema within PostgreSQL. 

![Entity Relationship Diagram](docs/erd.png)

The **Entity-Relationship Diagram (ERD)** above maps the domain constraints:
* **`media_assets`**: The source of truth for all binary files. It stores strict metadata (`s3_key`, `file_size_bytes`, `mime_type`) and an `asset_type` enum (e.g., *screenshot*, *avatar*, *cover*).
* **`news_articles`**: The central entity for content. It maintains a direct foreign key relationship to `media_assets` for its cover image (`cover_image_id`).
* **Tagging System**: A many-to-many relationship (`news_tags` <-> `article_tags`) allows flexible categorization and rapid filtering of the news feed.

---

## 3. API Specifications

### Synchronous (REST) Contracts

All REST boundaries adhere to Level 2 of the Richardson Maturity Model. 

| Method | Endpoint | Authorization | Description | Returns |
| :---: | :--- | :---: | :--- | :--- |
| `POST` | `/api/v1/media/upload` | `Bearer JWT` | Ingests a raw binary payload. Streams to S3. | `201 Created` |
| `GET`  | `/api/v1/media/{id}` | `Public` | Retrieves metadata and signed S3 URLs. | `200 OK` |
| `GET`  | `/api/v1/news` | `Public` | Retrieves paginated platform announcements. | `200 OK` |
| `POST` | `/api/v1/news` | `Admin JWT` | Authors a new article. Triggers RMQ events. | `201 Created` |

### Asynchronous (AMQP) Contracts

The service acts as an authoritative **Producer** for the `esports.news.exchange`. 

| Routing Key | Payload Type | Trigger Condition | Downstream Consumers |
| :--- | :--- | :--- | :--- |
| `news.published` | `application/json` | Admin invokes `POST /api/v1/news` | Notification Service |
| `news.archived` | `application/json` | Admin alters article status to archived. | Search Indexer |

**Example AMQP Payload (`NewsPublished`):**
```json
{
  "event_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "event_type": "NewsPublished",
  "timestamp": "2026-05-31T12:00:00Z",
  "data": {
    "article_id": "uuid",
    "title": "Grand Finals Announced!",
    "author_id": "uuid"
  }
}
```

---

## 4. Infrastructure & Configuration

> [!WARNING]
> **Production Parity:** Ensure that `JWT_SECRET_KEY` and S3 Access credentials are NEVER committed to version control. Inject them strictly via secure CI/CD pipelines or HashiCorp Vault.

### Strict Environment Requirements

The application enforces presence of environmental configurations via Pydantic `BaseSettings`. Failure to provide these parameters will result in a fatal boot sequence.

```env
# Persistence
DATABASE_URL=postgresql://media_user:password@media-db:5432/media_db

# Message Bus
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

# Object Storage Layer
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=media-bucket
```

### Initializing the Matrix

To cold-boot the entire infrastructure cluster (API, Postgres, MinIO, RMQ) for local verification, execute the orchestration command:

```bash
docker-compose up --build -d
```

---

## 5. Project Structure

A rigorous segregation of folders guarantees zero circular dependencies and maximum code predictability.

```text
media-service/
├── app/
│   ├── api/               # Interface Adapters (FastAPI HTTP Routers)
│   ├── core/              # Cross-Cutting Concerns (Exceptions, Telemetry)
│   ├── db/                # Persistence Layer (SQLAlchemy Models, ORM Repositories)
│   ├── domain/            # Enterprise Logic (Entities, Enums, Use-Cases)
│   ├── integrations/      # Infrastructure Adapters (Boto3/S3 Clients)
│   ├── messaging/         # Event Driven Adapters (Pika/RabbitMQ Producers)
│   ├── schemas/           # Data Transfer Objects (Pydantic Models)
│   ├── config.py          # Global State & Environment Loader
│   └── main.py            # ASGI Bootstrap Context
├── docs/                  # Architecture XMLs & API Schemas
├── alembic/               # Database migration scripts
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Local Container Topology
├── Dockerfile             # Production Image Definition
└── pyproject.toml         # Dependency & Build Graph
```

<div align="center">
  <sub>Built with precision for the Esports Hub Platform. Engineered for reliability.</sub>
</div>
