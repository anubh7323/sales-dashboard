-- Views for Tableau Consumption

-- View 1: Sales Summary
-- Consolidated view of sales with product details for general dashboarding
CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT 
    s.sales_id,
    s.date,
    s.region,
    p.product_name,
    p.category,
    s.quantity,
    s.revenue,
    (s.revenue - (s.quantity * p.price * 0.7)) AS estimated_profit -- Assuming 30% margin for demo
FROM Sales s
JOIN Product p ON s.product_id = p.product_id;

-- View 2: Inventory vs Sales
-- Pre-calculated gap analysis for inventory management
CREATE OR REPLACE VIEW vw_inventory_vs_sales AS
SELECT 
    i.inventory_id,
    p.product_name,
    p.category,
    i.warehouse_location,
    i.stock_level,
    (SELECT SUM(quantity) FROM Sales s WHERE s.product_id = p.product_id) AS total_lifetime_sales
FROM Inventory i
JOIN Product p ON i.product_id = p.product_id;

-- View 3: Region Performance
-- Aggregated metrics by region for map visualizations
CREATE OR REPLACE VIEW vw_region_performance AS
SELECT 
    region,
    COUNT(sales_id) AS transaction_count,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_order_value
FROM Sales
GROUP BY region;
