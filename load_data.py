import pandas as pd
from sqlalchemy import create_engine

DB_USER = "olist"
DB_PASSWORD = "olist123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

DATA_PATH = r"C:\Users\abc\Downloads\archive"

files_to_tables = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}

for filename, table_name in files_to_tables.items():
    file_path = f"{DATA_PATH}\\{filename}"
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"{table_name}: {len(df)} rows loaded")

print("done")