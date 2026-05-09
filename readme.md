# Store 205 Dashboard

A full-stack analytics dashboard for Store 205 sales, Systems RPU performance, and attach metrics.

This project was designed as a maintainable business intelligence platform focused on:
- Local store analytics first
- Associate-level operational insight
- Department-level performance tracking
- Chain-wide comparison second
- Long-term scalability and maintainability

---

# Project Goals

The primary purpose of this dashboard is to provide:
- Store 205 operational visibility
- Associate performance analysis
- Department performance analysis
- Systems RPU analytics
- MA Attach analytics
- Chain-wide benchmarking
- Executive-style dashboard reporting

The architecture prioritizes:
1. Local Store 205 data
2. Internal Store 205 comparisons
3. Chain-wide data
4. Chain-wide comparisons

---

# Current Features

## Sales Analytics
- Store sales summaries
- Department breakdowns
- No Sales ID tracking
- Store rankings
- Top store comparisons
- Daily / PPTD / MTD / QTD support

## Systems Analytics
- Systems summary metrics
- RPU analytics
- Attach RPU analytics
- Associate leaderboards
- Systems rankings
- Daily / PPTD / MTD support

## MA Attach Analytics
- MA attach summaries
- Associate attach performance
- Attach GM analysis
- Percentile tracking
- Daily / PPTD / MTD support

## Frontend Dashboard
- Multi-page dashboard architecture
- Responsive layouts
- Period switching
- Recharts visualizations
- Reusable dashboard components
- Type-safe API integration

---

# Tech Stack

## Backend
- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

## Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts
- Axios
- React Router DOM

---

# Project Structure

```text
store205-dashboard/
│
├── backend/
│   ├── analytics/
│   ├── api/
│   ├── database/
│   ├── imports/
│   ├── models/
│   ├── routes/
│   ├── scripts/
│   └── services/
│
├── data/
│   └── store205.db
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   └── tables/
│   │   ├── features/
│   │   │   ├── maAttach/
│   │   │   ├── sales/
│   │   │   └── systems/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── types/
│   │   └── utils/
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# Backend Architecture

The backend follows a layered architecture:

```text
Routes
→ Analytics Services
→ Database Queries
→ SQLite Database
```

The API layer is intentionally separated from analytics logic to improve:
- Maintainability
- Testability
- Scalability
- Future database migration support

---

# Frontend Architecture

The frontend follows a modular feature-based architecture.

```text
Pages
→ Feature Sections
→ Reusable Components
→ API Layer
→ Backend API
```

The frontend intentionally separates:
- Data fetching
- Presentation logic
- Reusable UI
- Formatting utilities
- Page orchestration

This minimizes coupling between the frontend and backend.

---

# API Overview

## Health

```http
GET /api/health
```

---

# Sales Endpoints

## Store Sales Summary

```http
GET /api/sales/store/{store_id}/{period_type}
```

## Department Breakdown

```http
GET /api/sales/store/{store_id}/{period_type}/departments
```

## No Sales Summary

```http
GET /api/sales/store/{store_id}/{period_type}/no-sales
```

## Store Sales Rankings

```http
GET /api/sales/store/{store_id}/{period_type}/rankings
```

## Top Stores by Sales

```http
GET /api/sales/top-stores/{period_type}
```

---

# Systems Endpoints

## Systems Summary

```http
GET /api/systems/store/{store_id}/{period_type}/summary
```

## Top RPU Associates

```http
GET /api/systems/store/{store_id}/{period_type}/top-rpu-associates
```

## Top Attach Associates

```http
GET /api/systems/store/{store_id}/{period_type}/top-attach-associates
```

## Top Systems Stores

```http
GET /api/systems/top-stores/{period_type}
```

## Systems Rankings

```http
GET /api/systems/store/{store_id}/{period_type}/rankings
```

---

# MA Attach Endpoints

## MA Attach Summary

```http
GET /api/ma-attach/store/{store_id}/{period_type}/summary
```

## Top MA Attach Associates

```http
GET /api/ma-attach/store/{store_id}/{period_type}/top-associates
```

---

# Supported Period Types

## Sales
- daily
- pay_period_to_date
- month_to_date
- quarter_to_date

## Systems
- daily
- pay_period_to_date
- month_to_date

## MA Attach
- daily
- pay_period_to_date
- month_to_date

---

# Validation

The backend includes:
- Input validation
- Period validation
- Limit validation
- Import validation
- Analytics validation
- API smoke testing

---

# Rebuild Pipeline

The project includes a complete rebuild pipeline:

```powershell
python scripts/rebuild_and_validate.py
```

This script:
1. Deletes the existing database
2. Recreates schema
3. Seeds base tables
4. Reimports all datasets
5. Runs validation scripts
6. Runs analytics tests

---

# API Smoke Testing

```powershell
python scripts/api_smoke_test.py
```

This validates:
- Endpoint availability
- Invalid route handling
- Status codes
- Backend integration

---

# Running the Backend

## Start FastAPI Server

```powershell
python -m uvicorn backend.app:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Frontend

## Install Dependencies

```powershell
npm install
```

## Start Development Server

```powershell
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# Frontend Design Philosophy

The frontend intentionally avoids:
- Giant cluttered dashboard pages
- Overloaded visualizations
- Excessive nested filtering
- Dense enterprise-style layouts

Instead, it uses:
- Overview-first design
- Focused analytics pages
- Clear information hierarchy
- Progressive detail expansion

---

# Current Frontend Pages

## Overview
High-level KPIs and rankings.

## Sales
Department breakdowns and store comparisons.

## Systems
RPU, attach performance, and associate analytics.

## MA Attach
MA attach analytics and associate performance.

---

# Maintainability Standards

This project prioritizes:
- Strong TypeScript typing
- Reusable UI components
- Feature-based organization
- Clear naming conventions
- Separation of concerns
- Backend/frontend decoupling
- Minimal duplicated logic

---

# Future Planned Features

## Planned Charts
- Systems attach charts
- Department trend charts
- Store comparison charts
- Associate performance charts

## Planned Analytics
- Historical trending
- Associate drilldown pages
- Store comparison dashboards
- Advanced percentile analysis

## Planned Infrastructure
- Authentication
- Role-based dashboards
- API caching
- Production deployment
- PostgreSQL migration support

---

# Development Notes

The project intentionally emphasizes:
- Correctness over speed
- Maintainability over shortcuts
- Scalable architecture
- Modular frontend growth
- Validation-first backend development

---

# License

This project is currently private and intended for portfolio, analytics, and internal dashboard development purposes.