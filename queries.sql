-------  SUPERSTORE PROJECT -- SQL SENTENCES ----------
------------------------------------------------------------------------------------
--- ***IMPORTANT: We are normalized de name of columns , this is the list of new names:
----- row_id, order_id, order_date, ship_date, ship_mode,customer_id, customer_name, segment, country, city, state, postal_code, region, product_id, category, sub-category,product_name, sales, quantity, discount, profit
-----------------------------------------------------------------------------------
-- QUERY 1 - Profit vs discount
SELECT 
    discount,
    AVG(profit) AS "AVG profit"
FROM superstore
GROUP BY discount
ORDER BY discount;

-- QUERY 2 - Unprofitable sub-categories
SELECT sub_category , SUM(profit) AS total_profit
FROM superstore
GROUP BY sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit;

-- QUERY 3 - Profit by category & region
SELECT category , region , SUM(profit) AS total_profit
FROM superstore
GROUP BY category, region
ORDER BY total_profit DESC;

-- QUERY 4 - High sales (>1000) , but low profit customers(<0)
SELECT customer_name , SUM(sales) AS total_sales ,SUM(profit) AS total_profit
FROM superstore
GROUP BY customer_name
HAVING SUM(sales) > 1000 AND SUM(profit) < 0
ORDER BY total_sales DESC;

-- QUERY 5 - Profit(avg profit & total profit) by category 
SELECT category, AVG(profit) AS avg_profit , SUM(profit) AS total_profit
FROM superstore
GROUP BY category
ORDER BY total_profit DESC;

-- QUERY 6 - Discount impact by segment in Profit
SELECT segment , discount , AVG(profit) AS avg_profit
FROM superstore
GROUP BY segment, discount
ORDER BY segment, discount;

-- QUERY 7 - Sales by region
SELECT region , SUM(sales) AS total_sales
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- QUERY 8 - Top 10 products by sales & profit
SELECT product_name , SUM(sales) AS total_sales, SUM(profit) AS total_profit
FROM superstore
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- QUERY 9 - Info of profit
SELECT MIN(profit) AS "MIN profit" , MAX(profit) AS "MAX profit" , AVG(profit) AS "AVG profit" , 
SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS "NUMBER OF NEGATIVE PROFIT ORDERS"
FROM superstore;


-- QUERY 10 - Quantity distribution
SELECT quantity , COUNT(*) AS order_count
FROM superstore
GROUP BY quantity
ORDER BY quantity;


