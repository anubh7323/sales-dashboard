import sqlite3
import pandas as pd
import os

# Configuration
DB_PATH = "../sales_dashboard.db"
DATA_DIR = "../data"
SQL_DIR = "../sql"

def get_connection():
    return sqlite3.connect(DB_PATH)

def execute_sql_file(conn, file_path):
    print(f"Executing {file_path}...")
    with open(file_path, 'r') as f:
        sql_script = f.read()
    
    # SQLite compatibility fixes
    # 1. Remove "OR REPLACE" from CREATE VIEW
    sql_script = sql_script.replace("CREATE OR REPLACE VIEW", "DROP VIEW IF EXISTS")
    
    # Split statements carefully (simple split by ;)
    statements = sql_script.split(';')
    
    cursor = conn.cursor()
    for statement in statements:
        if statement.strip():
            # For views, we might need to handle the DROP/CREATE split manually if we did a simple replace
            if "DROP VIEW IF EXISTS" in statement:
                # This is a hacky fix for the replace above. 
                # Better approach: Regex replace to split into two statements?
                # Or just handle the specific syntax for this project.
                
                # Let's try a more robust approach for the specific files we have.
                # If the statement starts with DROP VIEW IF EXISTS, it might be malformed because we replaced CREATE OR REPLACE
                # Actually, "CREATE OR REPLACE VIEW x" -> "DROP VIEW IF EXISTS x" is wrong.
                # It should be "DROP VIEW IF EXISTS x; CREATE VIEW x"
                pass 

    # Let's do a cleaner pass for compatibility
    clean_statements = []
    
    # Re-read for clean processing
    with open(file_path, 'r') as f:
        raw_sql = f.read()

    # Fix for Views
    if "CREATE OR REPLACE VIEW" in raw_sql:
        # We need to extract the view name to drop it first
        # This is getting complex for a simple script. 
        # Let's just use the replace and expect the user to run it on a fresh DB mostly.
        # Or better: Just use "CREATE VIEW IF NOT EXISTS" or drop first.
        
        # Simple replacement strategy for this specific project structure
        raw_sql = raw_sql.replace("CREATE OR REPLACE VIEW", "CREATE VIEW") 
        # Note: This will fail if view exists. We should drop tables/views at start of script.

    # Fix for Schema (MySQL specific types usually fine in SQLite, but let's be safe)
    # SQLite is very forgiving.
    
    statements = raw_sql.split(';')
    for stmt in statements:
        if stmt.strip():
            try:
                cursor.execute(stmt)
            except sqlite3.OperationalError as e:
                # Ignore "table already exists" if we are not dropping them
                if "already exists" in str(e):
                    print(f"  Warning: {e}")
                else:
                    print(f"  Error executing statement: {stmt[:50]}...")
                    print(f"  {e}")
    conn.commit()

def load_data(conn):
    print("Loading data from CSVs...")
    
    # Load Product
    df_product = pd.read_csv(os.path.join(DATA_DIR, 'Product.csv'))
    df_product.to_sql('Product', conn, if_exists='replace', index=False)
    print(f"  Loaded {len(df_product)} products.")

    # Load Inventory
    df_inventory = pd.read_csv(os.path.join(DATA_DIR, 'Inventory.csv'))
    df_inventory.to_sql('Inventory', conn, if_exists='replace', index=False)
    print(f"  Loaded {len(df_inventory)} inventory records.")

    # Load Sales
    df_sales = pd.read_csv(os.path.join(DATA_DIR, 'Sales.csv'))
    df_sales.to_sql('Sales', conn, if_exists='replace', index=False)
    print(f"  Loaded {len(df_sales)} sales records.")

def run_verification_queries(conn):
    print("\nRunning verification queries...")
    cursor = conn.cursor()
    
    # 1. Count records
    cursor.execute("SELECT COUNT(*) FROM Sales")
    print(f"  Total Sales Records: {cursor.fetchone()[0]}")
    
    # 2. Test View (Sales Summary)
    try:
        df = pd.read_sql_query("SELECT * FROM vw_sales_summary LIMIT 5", conn)
        print("\n  View: vw_sales_summary (First 5 rows)")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"  Error reading view: {e}")

def main():
    print("Setting up SQLite database...")
    
    # Remove old DB to ensure fresh start (handles the CREATE VIEW issue)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("  Removed existing database.")

    conn = get_connection()
    
    # 1. Create Schema
    # We can actually skip schema.sql if we use pandas to_sql, 
    # BUT schema.sql defines constraints (PK/FK) which pandas might not set perfectly.
    # Let's run schema first, then append data.
    execute_sql_file(conn, os.path.join(SQL_DIR, 'schema.sql'))
    
    # 2. Load Data
    # if_exists='append' to respect the schema we just created
    try:
        df_product = pd.read_csv(os.path.join(DATA_DIR, 'Product.csv'))
        df_product.to_sql('Product', conn, if_exists='append', index=False)
        
        df_inventory = pd.read_csv(os.path.join(DATA_DIR, 'Inventory.csv'))
        df_inventory.to_sql('Inventory', conn, if_exists='append', index=False)
        
        df_sales = pd.read_csv(os.path.join(DATA_DIR, 'Sales.csv'))
        df_sales.to_sql('Sales', conn, if_exists='append', index=False)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 3. Create Views
    # We need to fix the SQL for SQLite before running
    # Let's read the file, fix it in memory, and execute
    print("Creating views...")
    with open(os.path.join(SQL_DIR, 'views.sql'), 'r') as f:
        views_sql = f.read()
    
    # SQLite doesn't support CREATE OR REPLACE
    views_sql = views_sql.replace("CREATE OR REPLACE VIEW", "CREATE VIEW")
    
    cursor = conn.cursor()
    for stmt in views_sql.split(';'):
        if stmt.strip():
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"Error creating view: {e}")
    conn.commit()

    # 4. Verify
    run_verification_queries(conn)
    
    conn.close()
    print("\nDatabase setup complete: sales_dashboard.db")

if __name__ == "__main__":
    main()
