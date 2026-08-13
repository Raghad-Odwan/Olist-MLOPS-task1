# MLOps Training 2026/2027 - Task 1

## Get the Data Into a Database

This project is the first task of the MLOps training track. The goal is to take the Olist Brazilian E-Commerce dataset from raw CSV files and load it into a real relational database, then confirm that everything works through queries and joins.

## Dataset

The dataset used is the Brazilian E-Commerce Public Dataset by Olist, available on Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

It contains real e-commerce data split across nine related CSV files, covering orders, customers, products, sellers, payments, reviews, and geolocation.

| File | Table Name | Rows | Description |
|---|---|---|---|
| olist_orders_dataset.csv | orders | 99,441 | One order with purchase, approval, and delivery timestamps |
| olist_customers_dataset.csv | customers | 99,441 | Customer linked to an order, with city, state, and ZIP prefix |
| olist_order_items_dataset.csv | order_items | 112,650 | One item inside an order, with product, seller, and price |
| olist_order_payments_dataset.csv | order_payments | 103,886 | One payment record for an order |
| olist_order_reviews_dataset.csv | order_reviews | 99,224 | One customer review and score |
| olist_products_dataset.csv | products | 32,951 | One product, its category, weight, and dimensions |
| olist_sellers_dataset.csv | sellers | 3,095 | One seller and its location |
| olist_geolocation_dataset.csv | geolocation | 1,000,163 | Coordinates linked to Brazilian ZIP-code prefixes |
| product_category_name_translation.csv | category_translation | 71 | Category names translated from Portuguese to English |

## The Problem We Are Solving

The final goal of this project is to predict whether an order will be delivered late or on time. This task focuses only on the first step: understanding the data, building the database, loading the data, and confirming that everything works correctly.

## How the Tables Are Related

The tables are connected through shared key columns:

- order_id links orders, order_items, order_payments, and order_reviews
- customer_id links orders and customers
- product_id links order_items and products
- seller_id links order_items and sellers
- zip_code_prefix links customers, sellers, and geolocation

This means the data is not one flat table. It is a set of related tables, similar to a real company database. To build a single row per order later on for machine learning, the order_items and order_payments tables need to be aggregated first, since one order can have multiple items and multiple payment records.

## Project Structure

```
load_data.py       Loads all CSV files into PostgreSQL as tables
test_queries.py     Connects to the database and runs test queries and joins
report.md           This file
```

## Setup Process

### 1. Running PostgreSQL with Docker

PostgreSQL was run locally inside a Docker container using the following command:

```
docker run --name olist-db -e POSTGRES_USER=olist -e POSTGRES_PASSWORD=olist123 -e POSTGRES_DB=olist_db -p 5432:5432 -d postgres
```

This keeps the database isolated on the local machine and easy to reset if needed.

### 2. Loading the Data

The load_data.py script reads each CSV file using pandas and writes it into PostgreSQL as a table, using SQLAlchemy. Each file becomes one table with a matching name.

To run it:

```
python load_data.py
```

Expected output:

```
customers: 99441 rows loaded
geolocation: 1000163 rows loaded
order_items: 112650 rows loaded
order_payments: 103886 rows loaded
order_reviews: 99224 rows loaded
orders: 99441 rows loaded
products: 32951 rows loaded
sellers: 3095 rows loaded
category_translation: 71 rows loaded
done
```

### 3. Testing the Database

The test_queries.py script connects to the database and runs a set of queries to confirm that the tables and relationships work correctly. This includes listing all tables, reading sample rows, running several joins between related tables, and grouping data to check counts.

To run it:

```
python test_queries.py
```

The script performs the following checks:

- Lists all tables inside the database
- Reads the first rows from the orders table
- Joins orders with customers to see where each order was placed
- Joins orders, order_items, and products to see what was purchased
- Joins order_items with sellers to see who sold each item
- Joins orders with order_payments to see how each order was paid
- Joins orders with order_reviews to see customer feedback
- Groups orders by item count to find the largest orders
- Groups orders by status to see how many are delivered, shipped, canceled, and so on

## Problem Understanding

The main problem this project will try to solve later in the training is late delivery prediction: given the information available at the time an order is placed, predict whether it will arrive after the estimated delivery date.

This is a good first problem because:

- It has a clear binary target: the order is either late or on time
- It requires combining information from several tables, such as orders, items, products, sellers, and customer location
- It is easy to understand and explain, which makes it a good starting point before moving to harder problems

An important point for later steps: only information available before or at the time of purchase can be used as model input. Fields such as the actual delivery date or the review score happen after the order is placed, so using them directly would cause data leakage.

## Notes on the Database Password

The password used in this project (olist123) is a simple local development password for a PostgreSQL container running only on the local machine. It is not exposed to the internet and is used for learning purposes only. For a production setup, credentials like this should be stored in environment variables instead of being written directly in the code.

## Conclusion

At the end of this task, the database is running locally with all nine tables loaded correctly. The queries in test_queries.py confirm that the tables can be read and joined without errors, and the relationships between orders, customers, products, sellers, payments, and reviews all work as expected.

All the goals defined for this task have been achieved: the database is populated with real data, the relationships between tables are understood, and the target problem is clearly defined. This provides a solid foundation for the exploratory data analysis and feature engineering that will follow in the next stages of the project.
