# Store 205 Dashboard

## Overview

The Store 205 Dashboard is a backend-focused analytics project designed to transform the existing Store Daily Sales workbook into a more maintainable, queryable, and scalable reporting system.

The project preserves the structure and operational logic of the original workbook while enabling:

* Cleaner reporting
* Dashboard visualization
* Associate-level analytics
* Store-level comparisons
* Systems RPU analytics
* Import validation
* Future frontend/API integration

The goal is not to create fictional retail structures or demo-only analytics. The goal is to accurately represent real operational reporting data while improving usability and maintainability.

---

# Current Features

## Database Architecture

* Normalized SQLite schema
* Store table
* Department table
* Associate table
* Reporting periods table
* Import batch tracking
* Sales metrics table
* Systems RPU metrics table
* MA Attach metrics table (planned import support)

## Workbook Import Pipeline

### Sales Metrics Import

Imports:

* Daily
* PPTD
* MTD
* QTD

Preserves:

* Associate rows
* Store total rows
* Reporting periods
* Import history

### MS RPU Import

Imports:

* MS RPU Yesterday
* MS RPU MTD
* MS RPU PPTD

Tracks:

* Primary units
* ASP
* RPU
* Attach RPU
* Service plan attach percentages
* ESET attach percentages
* Office attach percentages
* Monitor attach percentages
* Mice and keyboard attach percentages
* All other attach percentages

## Validation Tooling

The project includes validation scripts to verify:

* Import row counts
* Reporting periods
* Store-level metrics
* Row types
* Import batches

---

# Project Structure

```text
store205-dashboard/
├── analytics/
├── data/
├── database/
│   ├── create_database.py
│   ├── db_helper.py
│   ├── schema.sql
│   ├── seed_database.py
│   ├── validate_sales_import.py
│   ├── validate_systems_rpu_import.py
│   └── verify_database.py
├── imports/
│   ├── excel_reader.py
│   ├── import_sales_metrics.py
│   ├── import_systems_rpu.py
│   ├── inspect_ms_rpu.py
│   └── inspect_workbook.py
├── .gitignore
└── README.md
```

---

# Tech Stack

| Technology         | Purpose                   |
| ------------------ | ------------------------- |
| Python             | Backend/import pipeline   |
| SQLite             | Analytics database        |
| openpyxl           | Excel workbook processing |
| Git                | Version control           |
| GitHub             | Repository hosting        |
| Visual Studio Code | Development environment   |

---

# Maintainability Standards

This project prioritizes maintainability over short-term speed.

Standards include:

* Clear file responsibilities
* Centralized database utilities
* Workbook validation before imports
* Reusable import helpers
* Structured schema comments
* Import audit tracking
* Explicit row classification
* Minimal hardcoding
* Readable function naming
* Modular importer design

When shortcuts or temporary implementations are used during development, they should be documented and refactored later.

---

# Workbook Design Principles

The workbook is treated as the source of truth.

Important operational constraints:

* Store 205 belongs to District 3.
* Stores are grouped by district, not region.
* Department codes come directly from the workbook.
* Unknown department display names remain nullable until verified.
* Associate rows and total rows are both preserved.
* Fake stores, regions, or departments should not be added.

---

# Setup Instructions

## 1. Clone Repository

```powershell
git clone https://github.com/OrionXJohnson/store205-dashboard.git
cd store205-dashboard
```

## 2. Install Dependencies

```powershell
pip install openpyxl
```

## 3. Create Database

```powershell
python database/create_database.py
python database/seed_database.py
```

## 4. Add Workbook

Place the workbook inside:

```text
data/
```

Recommended filename:

```text
Store-Daily-Sales.xlsx
```

Important:

The workbook is intentionally excluded from GitHub using `.gitignore`.

## 5. Run Imports

### Sales Metrics

```powershell
python imports/import_sales_metrics.py
```

### MS RPU Metrics

```powershell
python imports/import_systems_rpu.py
```

## 6. Validate Imports

```powershell
python database/validate_sales_import.py
python database/validate_systems_rpu_import.py
```

---

# Current Development Status

## Completed

* Database schema
* Workbook inspection tooling
* Sales metrics import pipeline
* Systems RPU import pipeline
* Import validation tooling
* GitHub integration
* Technical design documentation

## In Progress

* MA Attach importer
* Shared importer refactoring
* Backend analytics layer

## Planned

* FastAPI backend
* Dashboard frontend
* Query optimization
* Authentication/permissions
* Data visualization layer
* Store comparison dashboards
* Associate ranking dashboards
* Systems KPI dashboards

---

# Security Notes

This repository intentionally excludes:

* Real workbook files
* SQLite database files
* Sensitive operational data
* Credentials/API keys

Do not upload sensitive company data to the public repository.

---

# Future Goals

Planned future improvements include:

* Faster bulk imports
* Shared importer base classes
* Automated data cleaning
* Advanced analytics queries
* Historical trend analysis
* Performance optimization
* Frontend dashboard deployment
* Internal reporting tools

---

# License

This project is currently intended for educational, internship, and portfolio purposes.
