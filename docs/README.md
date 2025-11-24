# Sales Performance Dashboard (Tableau + SQL + Excel) -( https://sales-dashboard-for-me.streamlit.app/)

## Overview
This project is an end-to-end analytics solution designed to help leadership track revenue, regional sales, product performance, and inventory alignment. It utilizes SQL for data processing, Python for synthetic data generation, and Tableau for visualization.

## Project Structure
```
sales-performance-dashboard/
├── data/       # Raw & processed datasets (CSVs)
├── sql/        # SQL scripts for schema, queries, and views
├── scripts/    # Python scripts for data generation
├── docs/       # Documentation
└── tableau/    # Tableau workbook files
```

## Setup Instructions

### 1. Data Generation
To generate the initial dataset (Sales, Product, Inventory CSVs), run the Python script:
```bash
cd scripts
python generate_data.py
```
This will create `Sales.csv`, `Product.csv`, and `Inventory.csv` in the `data/` directory.

### 2. Database Setup
1. Import the generated CSV files into your SQL database (MySQL/PostgreSQL).
2. Run `sql/schema.sql` to ensure the table structures are correct (if not automatically created during import).
3. Run `sql/views.sql` to create the optimized views for Tableau.

### 3. Analytics & Visualization
- Use `sql/queries.sql` to run ad-hoc analysis on the database.
- Connect Tableau to your database (or the CSVs directly if preferred).
- Use the views `vw_sales_summary`, `vw_inventory_vs_sales`, and `vw_region_performance` as data sources.

## Key Metrics
- **Monthly Revenue Growth**: Tracks revenue trends and month-over-month growth percentage.
- **Region-wise Sales**: Compares performance across North, South, East, and West regions.
- **Product Category Performance**: Analyzes top-selling categories and average transaction values.
- **Inventory vs Sales Gap**: Highlights products with low stock levels but high recent sales volume.

## Tech Stack
- **SQL**: MySQL / PostgreSQL
- **Tableau**: Dashboarding & Visualization
- **Python**: Data Generation & ETL
- **Excel/CSV**: Initial Data Storage
