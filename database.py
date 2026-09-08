import sqlite3
import csv


DATABASE = "ecommerce.db"


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Remove old tables
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS products")

    # -------------------------
    # Customers table
    # -------------------------

    cursor.execute("""
        CREATE TABLE customers (
            CustomerID TEXT PRIMARY KEY,
            CustomerName TEXT NOT NULL,
            City TEXT NOT NULL
        )
    """)

    # -------------------------
    # Products table
    # -------------------------

    cursor.execute("""
        CREATE TABLE products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            Product TEXT NOT NULL,
            Category TEXT NOT NULL,
            Price REAL NOT NULL
        )
    """)

    # -------------------------
    # Orders table
    # -------------------------

    cursor.execute("""
        CREATE TABLE orders (
            OrderID INTEGER PRIMARY KEY,
            OrderDate TEXT NOT NULL,
            CustomerID TEXT NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            Price REAL NOT NULL,
            PaymentMethod TEXT NOT NULL,

            FOREIGN KEY (CustomerID)
                REFERENCES customers(CustomerID),

            FOREIGN KEY (ProductID)
                REFERENCES products(ProductID)
        )
    """)

    # Used to avoid duplicate products
    product_ids = {}

    # -------------------------
    # Read CSV
    # -------------------------

    with open("sales.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Insert customer
            cursor.execute("""
                INSERT OR IGNORE INTO customers
                (CustomerID, CustomerName, City)
                VALUES (?, ?, ?)
            """, (
                row["CustomerID"],
                row["CustomerName"],
                row["City"]
            ))

            # Create unique product key
            product_key = (
                row["Product"],
                row["Category"]
            )

            # Insert product only once
            if product_key not in product_ids:

                cursor.execute("""
                    INSERT INTO products
                    (Product, Category, Price)
                    VALUES (?, ?, ?)
                """, (
                    row["Product"],
                    row["Category"],
                    row["Price"]
                ))

                product_ids[product_key] = cursor.lastrowid

            product_id = product_ids[product_key]

            # Insert order
            cursor.execute("""
                INSERT INTO orders
                (
                    OrderID,
                    OrderDate,
                    CustomerID,
                    ProductID,
                    Quantity,
                    Price,
                    PaymentMethod
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row["OrderID"],
                row["OrderDate"],
                row["CustomerID"],
                product_id,
                row["Quantity"],
                row["Price"],
                row["PaymentMethod"]
            ))

    connection.commit()

    # -------------------------
    # Display database summary
    # -------------------------

    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    print("Database created successfully!")
    print(f"Customers: {customer_count}")
    print(f"Products: {product_count}")
    print(f"Orders: {order_count}")

    connection.close()


if __name__ == "__main__":
    create_database()