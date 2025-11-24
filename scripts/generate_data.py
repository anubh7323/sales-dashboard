import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configuration
DATA_DIR = "../data"
NUM_PRODUCTS = 50
NUM_SALES = 10000
REGIONS = ['North', 'South', 'East', 'West']
CATEGORIES = ['Electronics', 'Furniture', 'Clothing', 'Office Supplies', 'Home Decor']
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_products():
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        products.append({
            'product_id': f'P{i:03d}',
            'product_name': f'{category} Item {i}',
            'category': category,
            'price': round(random.uniform(10, 500), 2)
        })
    return pd.DataFrame(products)

def generate_inventory(products_df):
    inventory = []
    for _, row in products_df.iterrows():
        # Generate inventory for each product in random regions (or all)
        # Let's say each product is stocked in 1-3 regions
        stocked_regions = random.sample(REGIONS, k=random.randint(1, len(REGIONS)))
        
        for region in stocked_regions:
            inventory.append({
                'inventory_id': f"INV-{row['product_id']}-{region[0]}",
                'product_id': row['product_id'],
                'stock_level': random.randint(0, 500),
                'warehouse_location': f"{region} Warehouse"
            })
    return pd.DataFrame(inventory)

def generate_sales(products_df):
    sales = []
    product_ids = products_df['product_id'].tolist()
    product_prices = products_df.set_index('product_id')['price'].to_dict()
    
    date_range = (END_DATE - START_DATE).days
    
    for i in range(1, NUM_SALES + 1):
        date = START_DATE + timedelta(days=random.randint(0, date_range))
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        price = product_prices[product_id]
        revenue = round(quantity * price, 2)
        region = random.choice(REGIONS)
        
        sales.append({
            'sales_id': f'S{i:05d}',
            'product_id': product_id,
            'region': region,
            'quantity': quantity,
            'revenue': revenue,
            'date': date.strftime('%Y-%m-%d')
        })
    
    # Sort by date for realism
    sales_df = pd.DataFrame(sales)
    sales_df = sales_df.sort_values('date')
    return sales_df

def main():
    print("Generating data...")
    ensure_data_dir()
    
    # 1. Generate Products
    products_df = generate_products()
    products_path = os.path.join(DATA_DIR, 'Product.csv')
    products_df.to_csv(products_path, index=False)
    print(f"Generated {len(products_df)} products -> {products_path}")
    
    # 2. Generate Inventory
    inventory_df = generate_inventory(products_df)
    inventory_path = os.path.join(DATA_DIR, 'Inventory.csv')
    inventory_df.to_csv(inventory_path, index=False)
    print(f"Generated {len(inventory_df)} inventory records -> {inventory_path}")
    
    # 3. Generate Sales
    sales_df = generate_sales(products_df)
    sales_path = os.path.join(DATA_DIR, 'Sales.csv')
    sales_df.to_csv(sales_path, index=False)
    print(f"Generated {len(sales_df)} sales records -> {sales_path}")
    
    print("Data generation complete!")

if __name__ == "__main__":
    main()
