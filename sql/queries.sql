-- Analytics Queries for Sales Performance Dashboard

-- 1. Monthly Revenue Growth (Window Function)
-- Calculates total revenue per month and the percentage growth from the previous month
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(revenue) AS total_revenue,
    LAG(SUM(revenue)) OVER (ORDER BY DATE_FORMAT(date, '%Y-%m')) AS prev_month_revenue,
    (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY DATE_FORMAT(date, '%Y-%m'))) / 
    LAG(SUM(revenue)) OVER (ORDER BY DATE_FORMAT(date, '%Y-%m')) * 100 AS revenue_growth_pct
FROM Sales
GROUP BY DATE_FORMAT(date, '%Y-%m');

-- 2. Region-wise Sales Comparison
-- Aggregates total sales and revenue by region
SELECT 
    region,
    COUNT(sales_id) AS total_transactions,
    SUM(quantity) AS total_units_sold,
    SUM(revenue) AS total_revenue
FROM Sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 3. Product Category Performance
-- Joins Sales and Product tables to analyze performance by category
SELECT 
    p.category,
    COUNT(s.sales_id) AS sales_count,
    SUM(s.revenue) AS category_revenue,
    AVG(s.revenue) AS avg_transaction_value
FROM Sales s
JOIN Product p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 4. Inventory vs Sales Gap
-- Identifies products with low stock but high sales volume (potential stockouts)
WITH ProductSales AS (
    SELECT 
        product_id,
        SUM(quantity) AS total_sold_last_30_days
    FROM Sales
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY product_id
)
SELECT 
    p.product_name,
    i.warehouse_location,
    i.stock_level,
    COALESCE(ps.total_sold_last_30_days, 0) AS recent_sales,
    (i.stock_level - COALESCE(ps.total_sold_last_30_days, 0)) AS stock_gap
FROM Inventory i
JOIN Product p ON i.product_id = p.product_id
LEFT JOIN ProductSales ps ON i.product_id = ps.product_id
WHERE i.stock_level < 50 -- Low stock threshold
ORDER BY recent_sales DESC;
