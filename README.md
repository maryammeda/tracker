# VersoStack - Full-Stack Assignment & Task Tracker

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![React](https://img.shields.io/badge/React_19-20232A?style=flat&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL_17-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)

## Overview

**VersoStack** is a full-stack assignment and task management platform built for tracking schoolwork, deadlines, and personal items. It features a FastAPI backend with PostgreSQL, Redis caching, automated email reminders, and a modern React + TypeScript frontend with role-based access control.

---

## ⚙️ Features

### Assignment Management
- Create, update, and delete assignments with subject, title, due date, and priority tracking
- Mark assignments as complete/incomplete
- Results sorted by due date for at-a-glance deadline awareness
- Paginated listing with ownership-based access control

### Item Tracking
- General-purpose item CRUD for notes, resources, or anything else worth tracking
- Tied to user accounts with owner-based permissions
- Superusers can view and manage all items across users

### Authentication & Authorization
- JWT-based authentication with OAuth2 password flow
- User registration, login, and password recovery via email
- Role-based access control (regular users vs. superusers)
- Token expiration and secure password hashing with bcrypt

### Redis Caching
- Read-heavy assignment queries cached with a 5-minute TTL
- Automatic cache invalidation on create, update, and delete operations
- Graceful fallback — the app continues working if Redis is unavailable

### Automated Email Reminders
- Background scheduler (APScheduler) runs daily at 8:00 AM
- Sends reminder emails for assignments due the next day
- MJML-based responsive email templates for account creation, password reset, and reminders

### Admin Panel
- Superuser dashboard for managing all users
- Create, edit, and delete user accounts
- View all items and assignments across the platform

### Frontend
- React 19 with TypeScript and TanStack Router (file-based routing)
- Auto-generated API client from the backend's OpenAPI spec
- shadcn/ui components with Tailwind CSS styling
- Dark mode toggle with persistence
- Form validation with React Hook Form + Zod
- Toast notifications and loading states throughout

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, FastAPI, Uvicorn, SQLModel (SQLAlchemy + Pydantic) |
| **Database** | PostgreSQL 17, Alembic (migrations) |
| **Caching** | Redis |
| **Auth** | JWT (PyJWT), OAuth2, Bcrypt |
| **Scheduling** | APScheduler |
| **Email** | MJML templates, Jinja2, SMTP |
| **Frontend** | React 19, TypeScript, Vite, TanStack Router & Query |
| **UI** | shadcn/ui, Radix UI, Tailwind CSS, Lucide icons |
| **Monitoring** | Sentry |
| **DevOps** | Docker, Docker Compose, Traefik, GitHub Actions |
| **Testing** | Pytest (backend), Playwright (E2E) |

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React +   │────▶│   FastAPI    │────▶│ PostgreSQL  │
│  TypeScript  │◀────│   Backend   │◀────│     17      │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │    Redis    │
                    │    Cache    │
                    └─────────────┘
```

- **UUID primary keys** across all models for scalability
- **Cascade deletes** — removing a user cleans up all their items and assignments
- **Auto-generated TypeScript client** — frontend types stay in sync with the backend OpenAPI spec
- **Dependency injection** for database sessions, auth, and token validation

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.12+ (with `uv` package manager)

### Running with Docker

```bash
docker compose up -d
```

This starts PostgreSQL, Redis, the backend, frontend, Adminer (DB admin UI), and Traefik (reverse proxy).

### Running Locally

```bash
# Backend
cd backend
uv sync
fastapi dev app/main.py

# Frontend
cd frontend
npm install
npm run dev
```

### Generate Frontend API Client

```bash
cd frontend
npm run generate-client
```

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/routes/       # API endpoints (users, items, assignments, login)
│   │   ├── core/             # Config, security, DB, cache, email
│   │   ├── tasks/            # Background scheduler (reminders)
│   │   ├── models.py         # SQLModel database models
│   │   └── crud.py           # Database operations
│   ├── alembic/              # Database migrations
│   └── tests/                # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── routes/           # File-based routing (TanStack Router)
│   │   ├── components/       # UI components (shadcn/ui)
│   │   └── client/           # Auto-generated API client
│   └── tests/                # Playwright E2E tests
└── docker-compose.yml
```

---

## 🗺️ Roadmap

- [x] User authentication & JWT-based auth flow
- [x] Item CRUD with ownership and permissions
- [x] Assignment management with due dates and priorities
- [x] Redis caching layer
- [x] Automated daily email reminders (APScheduler)
- [x] React + TypeScript frontend with shadcn/ui
- [x] Docker Compose deployment with Traefik
- [x] CI/CD with GitHub Actions
- [ ] Knowledge graph visualization for assignments
- [ ] Calendar view for due dates
