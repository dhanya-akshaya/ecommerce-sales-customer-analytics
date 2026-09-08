import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# -----------------------------
# Customers
# -----------------------------

customers = []

first_names = [
    "Aarav", "Priya", "Rahul", "Ananya", "Arjun",
    "Sneha", "Vikram", "Meera", "Rohan", "Kavya",
    "Aditya", "Divya", "Kiran", "Neha", "Varun",
    "Pooja", "Sanjay", "Isha", "Nikhil", "Aisha"
]

cities = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Kochi"
]

for i in range(1, 151):
    name = random.choice(first_names) + " " + str(i)

    customers.append({
        "CustomerID": f"C{i:03}",
        "CustomerName": name,
        "City": random.choice(cities)
    })


# -----------------------------
# Products
# -----------------------------

products = [
    ("Laptop", "Electronics", 55000),
    ("Smartphone", "Electronics", 25000),
    ("Headphones", "Electronics", 2500),
    ("Keyboard", "Electronics", 1500),
    ("Mouse", "Electronics", 800),
    ("Monitor", "Electronics", 12000),
    ("Smartwatch", "Electronics", 5500),
    ("Tablet", "Electronics", 18000),

    ("T-Shirt", "Fashion", 900),
    ("Jeans", "Fashion", 1800),
    ("Dress", "Fashion", 2200),
    ("Shoes", "Fashion", 3000),
    ("Handbag", "Fashion", 2500),
    ("Saree", "Fashion", 3500),
    ("Jacket", "Fashion", 2800),

    ("Sofa", "Home", 22000),
    ("Chair", "Home", 2500),
    ("Table", "Home", 4500),
    ("Lamp", "Home", 1200),
    ("Bed", "Home", 18000),
    ("Wardrobe", "Home", 15000),

    ("Notebook", "Stationery", 200),
    ("Pen Set", "Stationery", 150),
    ("Backpack", "Stationery", 1200),
    ("Calculator", "Stationery", 700),

    ("Coffee Maker", "Appliances", 6500),
    ("Refrigerator", "Appliances", 32000),
    ("Air Conditioner", "Appliances", 42000),
    ("Microwave", "Appliances", 12000),

    ("Laptop Bag", "Accessories", 1800)
]


payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking"
]


# -----------------------------
# Generate Orders
# -----------------------------

start_date = datetime(2025, 1, 1)

rows = []

for order_id in range(10001, 11001):

    customer = random.choice(customers)

    product, category, base_price = random.choice(products)

    quantity = random.randint(1, 4)

    # Small random price variation
    price = round(
        base_price * random.uniform(0.90, 1.10),
        2
    )

    order_date = start_date + timedelta(
        days=random.randint(0, 608)
    )

    rows.append([
        order_id,
        order_date.strftime("%Y-%m-%d"),
        customer["CustomerID"],
        customer["CustomerName"],
        product,
        category,
        quantity,
        price,
        customer["City"],
        random.choice(payment_methods)
    ])


# -----------------------------
# Save CSV
# -----------------------------

with open(
    "sales.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "OrderID",
        "OrderDate",
        "CustomerID",
        "CustomerName",
        "Product",
        "Category",
        "Quantity",
        "Price",
        "City",
        "PaymentMethod"
    ])

    writer.writerows(rows)


print("Dataset generated successfully!")
print(f"Total orders: {len(rows)}")
print(f"Total customers: {len(customers)}")
print(f"Total products: {len(products)}")