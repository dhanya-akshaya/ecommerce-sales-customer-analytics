-- ==========================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- SQL BUSINESS ANALYSIS
-- ==========================================


-- 1. Total Revenue
SELECT
    ROUND(SUM(Quantity * Price), 2) AS total_revenue
FROM orders;


-- 2. Total Orders
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- 3. Total Customers
SELECT
    COUNT(*) AS total_customers
FROM customers;


-- 4. Revenue by Category
SELECT
    p.Category,
    ROUND(SUM(o.Quantity * o.Price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY revenue DESC;


-- 5. Top 10 Products by Revenue
SELECT
    p.Product,
    ROUND(SUM(o.Quantity * o.Price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.ProductID = p.ProductID
GROUP BY p.Product
ORDER BY revenue DESC
LIMIT 10;


-- 6. Top Customers by Spending
SELECT
    c.CustomerID,
    c.CustomerName,
    ROUND(SUM(o.Quantity * o.Price), 2) AS total_spending
FROM orders o
JOIN customers c
    ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY total_spending DESC
LIMIT 10;


-- 7. Monthly Revenue
SELECT
    strftime('%Y-%m', OrderDate) AS month,
    ROUND(SUM(Quantity * Price), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month;


-- 8. Revenue by City
SELECT
    c.City,
    ROUND(SUM(o.Quantity * o.Price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.CustomerID = c.CustomerID
GROUP BY c.City
ORDER BY revenue DESC;


-- 9. Payment Method Analysis
SELECT
    PaymentMethod,
    COUNT(*) AS orders,
    ROUND(SUM(Quantity * Price), 2) AS revenue
FROM orders
GROUP BY PaymentMethod
ORDER BY revenue DESC;


-- 10. Customer Purchase Frequency
SELECT
    c.CustomerID,
    c.CustomerName,
    COUNT(o.OrderID) AS number_of_orders,
    ROUND(SUM(o.Quantity * o.Price), 2) AS total_spending
FROM customers c
JOIN orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY number_of_orders DESC;


-- 11. Average Order Value by Customer
SELECT
    c.CustomerID,
    c.CustomerName,
    ROUND(
        AVG(o.Quantity * o.Price),
        2
    ) AS average_order_value
FROM customers c
JOIN orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY average_order_value DESC;


-- 12. Category Ranking
WITH category_sales AS (

    SELECT
        p.Category,
        SUM(o.Quantity * o.Price) AS revenue
    FROM orders o
    JOIN products p
        ON o.ProductID = p.ProductID
    GROUP BY p.Category
)

SELECT
    Category,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS category_rank
FROM category_sales;


-- 13. Monthly Revenue Growth
WITH monthly_sales AS (

    SELECT
        strftime('%Y-%m', OrderDate) AS month,
        SUM(Quantity * Price) AS revenue
    FROM orders
    GROUP BY month
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,

    ROUND(
        (
            revenue -
            LAG(revenue) OVER (
                ORDER BY month
            )
        )
        /
        LAG(revenue) OVER (
            ORDER BY month
        ) * 100,
        2
    ) AS growth_percentage

FROM monthly_sales
ORDER BY month;