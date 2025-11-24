import sqlite3
import pandas as pd
import os

# Configuration
DB_PATH = "../sales_dashboard.db"
QUERIES_FILE = "../sql/queries.sql"

def run_analysis():
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    print(f"Reading queries from {QUERIES_FILE}...")
    with open(QUERIES_FILE, 'r') as f:
        sql_content = f.read()
        
    # Split queries by semicolon
    # Note: This is a simple splitter and might break on complex SQL with semicolons in strings
    queries = sql_content.split(';')
    print(f"Found {len(queries)} potential queries.")
    
    for i, query in enumerate(queries):
        query = query.strip()
        if not query:
            continue
            
        # Extract a title from comments if possible
        lines = query.split('\n')
        title = f"Query {i+1}"
        for line in lines:
            if line.strip().startswith('--'):
                title = line.strip().replace('--', '').strip()
                break
        
        print(f"\n{'='*50}")
        print(f"Running: {title}")
        print(f"{'='*50}")
        
        try:
            # SQLite compatibility fixes
            sqlite_query = query
            
            # Specific fixes first
            if "DATE_SUB(CURDATE(), INTERVAL 30 DAY)" in sqlite_query:
                sqlite_query = sqlite_query.replace("DATE_SUB(CURDATE(), INTERVAL 30 DAY)", "DATE('now', '-30 days')")
            
            # General fixes
            sqlite_query = sqlite_query.replace("DATE_FORMAT(date, '%Y-%m')", "strftime('%Y-%m', date)")
            sqlite_query = sqlite_query.replace("CURDATE()", "DATE('now')")
            # Be careful with generic DATE_SUB replacement if we haven't handled the INTERVAL part
            
            df = pd.read_sql_query(sqlite_query, conn)
            if df.empty:
                print("No results found.")
            else:
                print(df.to_string(index=False))
                
        except Exception as e:
            print(f"Error executing query: {e}")
            print(f"Original Query snippet: {query[:100]}...")

    conn.close()

if __name__ == "__main__":
    run_analysis()
