-- Schema for Sales Performance Dashboard

-- Table: Product
-- Stores product details including category and pricing
CREATE TABLE IF NOT EXISTS Product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL
);

-- Table: Inventory
-- Tracks stock levels and warehouse locations for products
CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50),
    stock_level INT NOT NULL,
    warehouse_location VARCHAR(100),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Table: Sales
-- Records individual sales transactions linked to products
CREATE TABLE IF NOT EXISTS Sales (
    sales_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50),
    region VARCHAR(50),
    quantity INT NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);
