/*
Store 205 Dashboard Database Schema

Purpose:
This schema supports a dashboard that mirrors the Store Daily Sales workbook
while allowing a more sophisticated UI and analytics layer.

Design goals:
- Preserve associate-level rows and total rows.
- Store real department codes from the workbook.
- Track imports for auditability.
- Separate sales, MS RPU, and MA Attach metrics.
- Avoid invented stores, regions, or departments.
*/

PRAGMA foreign_keys = ON;


/* =========================
   STORES
   ========================= */

CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    district_number INTEGER,
    store_type TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);


/* =========================
   DEPARTMENTS
   ========================= */

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_code TEXT NOT NULL UNIQUE,
    department_display_name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);


/* =========================
   ASSOCIATES
   ========================= */

CREATE TABLE IF NOT EXISTS associates (
    associate_id INTEGER PRIMARY KEY AUTOINCREMENT,

    first_name TEXT,
    last_name TEXT,

    /*
    Some workbook sheets include an employee/code value.
    This is nullable because not every row has one.
    */
    employee_code TEXT UNIQUE,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);


/* =========================
   REPORTING PERIODS
   ========================= */

CREATE TABLE IF NOT EXISTS reporting_periods (
    period_id INTEGER PRIMARY KEY AUTOINCREMENT,

    report_date TEXT NOT NULL,

    period_type TEXT NOT NULL CHECK (
        period_type IN (
            'daily',
            'pay_period_to_date',
            'month_to_date',
            'quarter_to_date'
        )
    ),

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (report_date, period_type)
);


/* =========================
   IMPORT BATCHES
   ========================= */

CREATE TABLE IF NOT EXISTS import_batches (
    import_batch_id INTEGER PRIMARY KEY AUTOINCREMENT,

    source_file_name TEXT NOT NULL,
    source_sheet_name TEXT NOT NULL,

    report_date TEXT,
    period_type TEXT,

    imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
    row_count INTEGER DEFAULT 0,

    notes TEXT
);


/* =========================
   DAILY / PPTD / MTD / QTD SALES METRICS
   ========================= */

CREATE TABLE IF NOT EXISTS sales_metrics (
    sales_metric_id INTEGER PRIMARY KEY AUTOINCREMENT,

    import_batch_id INTEGER,

    store_id INTEGER NOT NULL,
    department_id INTEGER,
    associate_id INTEGER,
    period_id INTEGER NOT NULL,

    /*
    Preserves workbook row meaning.

    Examples:
    - associate
    - department_total
    - store_total
    - no_sales_id
    - goal
    - minimum
    */
    row_type TEXT NOT NULL DEFAULT 'associate',

    sales_amount REAL DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,

    service_plan_quantity INTEGER DEFAULT 0,
    service_plan_sales REAL DEFAULT 0,
    service_plan_percent REAL DEFAULT 0,

    rank_value INTEGER,

    nordvpn_quantity INTEGER DEFAULT 0,
    nordvpn_sales REAL DEFAULT 0,

    eset_quantity INTEGER DEFAULT 0,
    eset_percent REAL DEFAULT 0,
    eset_perm_gm_per_unit REAL DEFAULT 0,

    office_quantity INTEGER DEFAULT 0,
    office_ratio REAL DEFAULT 0,

    priority_care_quantity INTEGER DEFAULT 0,
    priority_care_ratio REAL DEFAULT 0,

    service_quantity INTEGER DEFAULT 0,
    service_upt REAL DEFAULT 0,
    service_gm_per_unit REAL DEFAULT 0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (import_batch_id)
        REFERENCES import_batches(import_batch_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id),

    FOREIGN KEY (associate_id)
        REFERENCES associates(associate_id),

    FOREIGN KEY (period_id)
        REFERENCES reporting_periods(period_id)
);


/* =========================
   MICRO CENTER SYSTEMS RPU METRICS
   ========================= */

CREATE TABLE IF NOT EXISTS systems_rpu_metrics (
    systems_rpu_metric_id INTEGER PRIMARY KEY AUTOINCREMENT,

    import_batch_id INTEGER,

    store_id INTEGER NOT NULL,
    associate_id INTEGER,
    period_id INTEGER NOT NULL,

    row_type TEXT NOT NULL DEFAULT 'associate',

    primary_units INTEGER DEFAULT 0,
    asp REAL DEFAULT 0,
    rpu REAL DEFAULT 0,

    total_attach_units INTEGER DEFAULT 0,
    total_attach_rpu REAL DEFAULT 0,

    service_plans_attach_percent REAL DEFAULT 0,
    eset_attach_percent REAL DEFAULT 0,
    office_attach_percent REAL DEFAULT 0,
    monitors_attach_percent REAL DEFAULT 0,
    mice_keyboard_attach_percent REAL DEFAULT 0,
    all_other_attach_percent REAL DEFAULT 0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (import_batch_id)
        REFERENCES import_batches(import_batch_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    FOREIGN KEY (associate_id)
        REFERENCES associates(associate_id),

    FOREIGN KEY (period_id)
        REFERENCES reporting_periods(period_id)
);


/* =========================
   MICRO CENTER APPLE ATTACH METRICS
   ========================= */

CREATE TABLE IF NOT EXISTS ma_attach_metrics (
    ma_attach_metric_id INTEGER PRIMARY KEY AUTOINCREMENT,

    import_batch_id INTEGER,

    store_id INTEGER NOT NULL,
    associate_id INTEGER,
    period_id INTEGER NOT NULL,

    row_type TEXT NOT NULL DEFAULT 'associate',

    computers INTEGER DEFAULT 0,
    upt REAL DEFAULT 0,

    attach_revenue REAL DEFAULT 0,
    attach_gm REAL DEFAULT 0,

    eset_quantity INTEGER DEFAULT 0,
    office_quantity INTEGER DEFAULT 0,
    service_plan_quantity INTEGER DEFAULT 0,

    eset_percentile REAL DEFAULT 0,
    office_percentile REAL DEFAULT 0,
    service_plan_percentile REAL DEFAULT 0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (import_batch_id)
        REFERENCES import_batches(import_batch_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    FOREIGN KEY (associate_id)
        REFERENCES associates(associate_id),

    FOREIGN KEY (period_id)
        REFERENCES reporting_periods(period_id)
);