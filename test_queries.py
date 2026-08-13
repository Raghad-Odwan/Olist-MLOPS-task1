from sqlalchemy import create_engine, text

# Database connection settings (same as the docker run command)
DB_USER = "olist"
DB_PASSWORD = "olist123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

with engine.connect() as conn:

    # Show all tables inside the database
    print("List of tables:")
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    for row in result:
        print(" -", row[0])

    # Simple query: read a few rows from the orders table
    print("\nFirst 5 orders:")
    result = conn.execute(text("SELECT order_id, customer_id, order_status FROM orders LIMIT 5"))
    for row in result:
        print(row)

    # Join orders with customers to see where each order was placed
    print("\nJoin orders with customers:")
    query = """
        SELECT o.order_id, o.order_status, c.customer_city, c.customer_state
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Join orders with order_items and products to see what was bought
    print("\nJoin orders with items and products:")
    query = """
        SELECT o.order_id, oi.product_id, p.product_category_name, oi.price, oi.freight_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Join order_items with sellers to see who sold each item
    print("\nJoin order items with sellers:")
    query = """
        SELECT oi.order_id, oi.seller_id, s.seller_city, s.seller_state, oi.price
        FROM order_items oi
        JOIN sellers s ON oi.seller_id = s.seller_id
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Join orders with payments to see how each order was paid
    print("\nJoin orders with payments:")
    query = """
        SELECT o.order_id, op.payment_type, op.payment_value, op.payment_installments
        FROM orders o
        JOIN order_payments op ON o.order_id = op.order_id
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Join orders with reviews to see customer feedback
    print("\nJoin orders with reviews:")
    query = """
        SELECT o.order_id, r.review_score, r.review_comment_message
        FROM orders o
        JOIN order_reviews r ON o.order_id = r.order_id
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Group by: count how many items each order has
    print("\nOrders with the most items:")
    query = """
        SELECT o.order_id, COUNT(oi.order_id) as item_count
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY o.order_id
        ORDER BY item_count DESC
        LIMIT 5
    """
    for row in conn.execute(text(query)):
        print(row)

    # Group by: count orders per status
    print("\nCount orders by status:")
    query = "SELECT order_status, COUNT(*) FROM orders GROUP BY order_status"
    for row in conn.execute(text(query)):
        print(row)

print("\nAll queries and joins completed successfully!")