# Data Generation Walkthrough

I have successfully verified the project setup and generated the synthetic data required for the Sales Performance Dashboard.

## 1. Environment Setup
- Verified Python 3.13 installation.
- Installed required dependencies: `pandas`, `numpy`.

## 2. Data Generation
Ran the `scripts/generate_data.py` script to create the following datasets in the `data/` directory:

| File | Size | Records | Description |
|------|------|---------|-------------|
| `Product.csv` | ~2KB | 50 | Product details (ID, Name, Category, Price) |
| `Inventory.csv` | ~4KB | 120 | Stock levels per warehouse |
| `Sales.csv` | ~380KB | 10,000 | Transactional sales data (2023-2024) |

## 3. Data Verification
Sample of generated `Sales.csv`:
```csv
sales_id,product_id,region,quantity,revenue,date
S04434,P017,West,9,1881.72,2023-01-01
S05872,P008,West,3,1307.67,2023-01-01
S06837,P041,North,10,4041.8,2023-01-01
```

## 4. Database Verification (SQLite)
Created a local SQLite database `sales_dashboard.db` to verify the schema and views.

### Execution Log
```bash
> python scripts/setup_db.py
Setting up SQLite database...
Executing ../sql\schema.sql...
Data loaded successfully.
Creating views...
Running verification queries...
  Total Sales Records: 10000
```

### View Verification (`vw_sales_summary`)
| sales_id | date | region | product_name | category | quantity | revenue | estimated_profit |
|---|---|---|---|---|---|---|---|
| S04434 | 2023-01-01 | West | Clothing Item 17 | Clothing | 9 | 1881.72 | 564.516 |
| S05872 | 2023-01-01 | West | Electronics Item 8 | Electronics | 3 | 1307.67 | 392.301 |

## Conclusion
The project is fully set up and verified.
- **Data**: Generated and validated.
- **Schema**: Applied and tested.
- **Views**: Created and querying correctly.

You can now use `sales_dashboard.db` for local analysis or proceed to deploy the SQL scripts to a production server.

## 5. Frontend Dashboard (Streamlit)
A interactive dashboard has been built to visualize the data.

### Features
- **KPIs**: Total Revenue, Transactions, Avg Order Value.
- **Interactive Charts**: Revenue trends, Regional sales, Top products.
- **Filters**: Date range, Region, Category.

### How to Run
```bash
streamlit run dashboard/app.py
```
This will open the dashboard in your default web browser (usually at `http://localhost:8501`).

> [!NOTE]
> The first time you run Streamlit, it may ask for your email. You can simply press **Enter** to skip this step.
