import os
import sqlite3
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "text_to_sql.db")

# Maps CSV filename -> SQL table name
CSV_TABLE_MAP = {
    "Budgets.csv": "budgets",
    "Products.csv": "products",
    "Regions.csv": "regions",
    "SRegions.csv": "sregions",
    "Sales_Orders_old.csv": "sales_orders",
    "customers.csv": "customers",
    "order.csv": "orders",
}


def build_database():
    """Builds (or rebuilds) the SQLite database from all CSVs in data/."""
    conn = sqlite3.connect(DB_PATH)
    for csv_file, table_name in CSV_TABLE_MAP.items():
        csv_path = os.path.join(DATA_DIR, csv_file)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded {csv_file} -> table '{table_name}' ({len(df)} rows)")
        else:
            print(f"Skipped {csv_file} — file not found")
    conn.close()


if __name__ == "__main__":
    build_database()
