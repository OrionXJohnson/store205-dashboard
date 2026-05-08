# Store 205 Dashboard

A backend analytics and dashboard project for transforming the Store Daily Sales workbook into a structured, queryable, and dashboard-ready reporting system.

The project is designed around real Store 205 workbook data and focuses on accuracy, maintainability, and future dashboard deployment.

---

## Project Purpose

The Store 205 Dashboard is being built to make existing store reporting easier to analyze, validate, and eventually visualize through a more sophisticated user interface.

The goal is not to create fake demo data or fictional business categories. The goal is to preserve the workbook’s real operational structure while improving:

- Data organization
- Reporting accuracy
- Store-level visibility
- Department-level visibility
- Systems performance analysis
- Apple attach analysis
- Associate performance analysis
- Cross-store comparisons
- Future dashboard usability

---

## Current Project Status

The project currently includes a working backend data platform foundation.

Completed so far:

- SQLite database schema
- Seeded store and department lookup data
- Sales workbook importer
- Systems RPU importer
- MA Attach importer
- Shared importer helper functions
- Import batch tracking
- Sales analytics layer
- Systems analytics layer
- Validation scripts
- Full rebuild and validation pipeline
- Git/GitHub workflow
- Documentation structure

The next planned major phase is the API layer.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend scripts, importers, analytics logic |
| SQLite | Local analytics database |
| openpyxl | Excel workbook parsing |
| Git | Version control |
| GitHub | Repository hosting |
| Visual Studio Code | Development environment |

Planned:

| Technology | Purpose |
|---|---|
| Flask or FastAPI | Backend API layer |
| React | Frontend dashboard |
| Charting library | Dashboard visualizations |

---

## Project Architecture

Current backend flow:

```text
Excel Workbook
    ↓
Import Scripts
    ↓
SQLite Database
    ↓
Analytics Layer
    ↓
Validation/Test Scripts
```

Planned full application flow:

```text
Excel Workbook
    ↓
Import Scripts
    ↓
SQLite Database
    ↓
Analytics Layer
    ↓
API Layer
    ↓
Frontend Dashboard
```

---

## Project Structure

```text
store205-dashboard/
├── analytics/
│   ├── inspect_sales_totals.py
│   ├── inspect_systems_totals.py
│   ├── sales_analytics.py
│   ├── systems_analytics.py
│   ├── test_sales_analytics.py
│   └── test_systems_analytics.py
│
├── data/
│   ├── Store-Daily-Sales.xlsx
│   └── store205.db
│
├── database/
│   ├── create_database.py
│   ├── db_helper.py
│   ├── schema.sql
│   ├── seed_database.py
│   ├── validate_ma_attach_import.py
│   ├── validate_sales_import.py
│   ├── validate_systems_rpu_import.py
│   └── verify_database.py
│
├── imports/
│   ├── excel_reader.py
│   ├── import_helpers.py
│   ├── import_ma_attach.py
│   ├── import_sales_metrics.py
│   ├── import_systems_rpu.py
│   ├── inspect_ma_attach.py
│   ├── inspect_ms_rpu.py
│   ├── inspect_sales_row_types.py
│   └── inspect_workbook.py
│
├── scripts/
│   └── rebuild_and_validate.py
│
├── .gitignore
└── README.md
```

---

## Data Source

The primary source of truth is the Store Daily Sales workbook.

Expected local workbook location:

```text
data/Store-Daily-Sales.xlsx
```

The workbook is not committed to GitHub because it may contain sensitive operational or employee-related data.

---

## Important Business Rules

This project follows the actual workbook structure.

Current confirmed rules:

- Store 205 belongs to District 3.
- Stores are grouped by district, not region.
- Store and department structures should come from the workbook.
- Fake stores, fake departments, fake regions, or fictional categories should not be added.
- Department codes should only be interpreted when confirmed.
- Unknown department names should remain unconfirmed until verified.
- Store totals, department totals, associate rows, and No Sales ID rows must be handled separately.

Confirmed department display names:

| Code | Display Name |
|---|---|
| BY | Build Your Own |
| MS | Systems |
| MA | Apple |
| GS | General Sales |
| CE | Consumer Electronics |
| SE | Service |
| OP | Operations |

Other department codes are currently preserved as unconfirmed until verified.

---

## Database Design

The SQLite database currently stores:

- Stores
- Departments
- Associates
- Reporting periods
- Import batches
- Sales metrics
- Systems RPU metrics
- MA Attach metrics

The database also includes indexes to improve analytics query speed.

Common indexed fields include:

- `store_id`
- `period_id`
- `row_type`
- `department_id`
- `associate_id`

---

## Import Pipeline

The project currently imports three major workbook sections.

### Sales Metrics Import

Script:

```powershell
python imports/import_sales_metrics.py
```

Imports:

- Daily
- PPTD
- MTD
- QTD

Preserves row types:

- `associate`
- `department_total`
- `no_sales_id`
- `no_sales_total`
- `store_total`

Important distinction:

`No Sales ID` is treated as an operational/unattributed sales category. It may represent web pickup, unattributed transactions, register-only activity, or transactions not tied to an associate label.

### Systems RPU Import

Script:

```powershell
python imports/import_systems_rpu.py
```

Imports:

- MS RPU Yesterday
- MS RPU MTD
- MS RPU PPTD

Tracks:

- Primary units
- ASP
- RPU
- Attach units per primary
- Total Attach RPU
- Service plan attach percentage
- ESET attach percentage
- Office attach percentage
- Monitor attach percentage
- Mice/keyboard attach percentage
- All other attach percentage

Important naming note:

The workbook’s Total Attach → Units column is stored as:

```text
attach_units_per_primary
```

This represents average attached items per primary item sold, not a raw total attach count.

### MA Attach Import

Script:

```powershell
python imports/import_ma_attach.py
```

Imports:

- MA Attach Yesterday
- MA Attach PPTD
- MA Attach MTD

Tracks:

- Computers
- UPT
- Attach revenue
- Attach GM$
- ESET quantity
- Office quantity
- Service plan quantity
- Attach revenue per PC metrics
- Percentile metrics

---

## Analytics Layer

Analytics modules are designed to keep business logic separate from raw database queries.

### Sales Analytics

File:

```text
analytics/sales_analytics.py
```

Current capabilities:

- Store sales summary
- Department sales breakdown
- No Sales ID summary
- Store sales rankings
- Store sales comparisons

Example business questions supported:

- How much did Store 205 sell today, MTD, PPTD, or QTD?
- Which departments are driving sales?
- How much sales volume is unattributed through No Sales ID?
- How does Store 205 rank against other stores?
- Is Store 205 high volume, high average transaction, or both?

### Systems Analytics

File:

```text
analytics/systems_analytics.py
```

Current capabilities:

- Store Systems KPI summary
- Top RPU associates
- Top Attach RPU associates
- Store Systems RPU comparison
- Store Systems ranking by selected metrics

Example business questions supported:

- How strong is Store 205 in Systems RPU?
- Which associates lead in RPU?
- Which associates lead in Attach RPU?
- How does Store 205 compare against other stores?
- Is Store 205 high volume, high quality, or both?

---

## Validation Workflow

Validation scripts are included to verify imports and catch regressions.

Run individual validations:

```powershell
python database/verify_database.py
python database/validate_sales_import.py
python database/validate_systems_rpu_import.py
python database/validate_ma_attach_import.py
```

Run analytics tests:

```powershell
python analytics/test_sales_analytics.py
python analytics/test_systems_analytics.py
```

---

## Full Rebuild and Validation

The main backend health-check command is:

```powershell
python scripts/rebuild_and_validate.py
```

This script:

- Deletes the existing local SQLite database
- Recreates the database schema
- Seeds lookup data
- Imports Sales metrics
- Imports Systems RPU metrics
- Imports MA Attach metrics
- Runs database verification
- Runs import validation scripts
- Runs analytics test scripts
- Stops immediately if a command fails

This is the recommended command before committing major backend changes.

---

## Setup Instructions

### 1. Clone the Repository

```powershell
git clone https://github.com/OrionXJohnson/store205-dashboard.git
cd store205-dashboard
```

### 2. Install Python Dependencies

```powershell
pip install openpyxl
```

### 3. Add the Workbook Locally

Place the workbook here:

```text
data/Store-Daily-Sales.xlsx
```

The workbook is intentionally ignored by Git.

### 4. Rebuild and Validate the Backend

```powershell
python scripts/rebuild_and_validate.py
```

If the script finishes successfully, the local backend database and analytics layer are functioning.

---

## Git Workflow

Recommended workflow after each stable milestone:

```powershell
git add .
git commit -m "Describe the completed change"
git push
```

Good commit message examples:

```text
Fix sales row type classification
Add Systems analytics leaderboards
Refactor MA Attach importer shared helpers
Add rebuild and validation pipeline
```

Avoid vague commit messages such as:

```text
update
changes
stuff
```

---

## Security Notes

This repository should not include:

- Real Excel workbook files
- SQLite database files
- Employee-sensitive data
- Store operational exports
- API keys
- Passwords
- Credentials

The following are intentionally ignored by Git:

```text
data/*.xlsx
data/*.db
.env
.venv/
__pycache__/
```

---

## Maintainability Standards

This project prioritizes maintainability over quick shortcuts.

Standards:

- Use clear file responsibilities.
- Keep import logic separate from analytics logic.
- Keep analytics logic separate from future API/frontend code.
- Avoid hardcoding business assumptions unless verified.
- Preserve workbook structure accurately.
- Use shared helper functions where appropriate.
- Add comments when logic may not be obvious later.
- Prefer readable code over overly clever code.
- Validate data after refactors.
- Commit stable checkpoints frequently.

If a shortcut is ever used, it should be documented along with how to improve it later.

---

## Current Known Notes

- PPTD and MTD currently match in the workbook data used during development.
- Some department codes remain unconfirmed.
- `No Sales ID` is a valid operational category and should not be treated as junk data.
- `attach_units_per_primary` is not a raw count; it is an average-style attach metric from the workbook.
- Some inspection scripts are retained intentionally because the workbook structure is still being studied.

---

## Roadmap

### Completed

- Database schema
- Seed data
- Sales import pipeline
- Systems RPU import pipeline
- MA Attach import pipeline
- Shared import helpers
- Sales analytics
- Systems analytics
- Database indexes
- Validation scripts
- Rebuild and validation pipeline
- GitHub workflow

### Next

- API layer
- API route organization
- JSON response contracts
- Sales dashboard endpoints
- Systems dashboard endpoints

### Future

- Frontend dashboard
- Store executive overview page
- Department drill-down pages
- Systems drill-down page
- MA Attach drill-down page
- Cross-store comparison views
- Associate performance views
- Role-based dashboard views
- Deployment planning

---

## Planned API Direction

The next phase will expose analytics through backend endpoints.

Planned flow:

```text
Frontend
    ↓
API routes
    ↓
Analytics functions
    ↓
SQLite database
```

Example future endpoints:

```text
GET /api/sales/store/205/daily
GET /api/sales/store/205/month_to_date
GET /api/systems/store/205/daily
GET /api/systems/store/205/month_to_date
```

The frontend should not query SQLite directly.

---

## Project Philosophy

This project is being built as a real analytics system, not a mock dashboard.

The guiding principles are:

- Accuracy first
- Workbook alignment
- Maintainable code
- Honest business interpretation
- Clear separation of concerns
- Repeatable validation
- No fictional data structures
- Dashboard-ready backend design

The final dashboard should help managers understand store performance more clearly while still respecting how the workbook actually reports the business.

---

# License

This project is currently intended for educational, internship, and portfolio purposes.
