from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "ecommerce.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(ValueError)
def handle_value_error(error):

    return jsonify({
        "error": "Invalid filter",
        "message": str(error)
    }), 400


@app.errorhandler(sqlite3.Error)
def handle_database_error(error):

    print("Database error:", error)

    return jsonify({
        "error": "Database error",
        "message": "Unable to retrieve data from the database."
    }), 500


@app.errorhandler(404)
def handle_not_found(error):

    return jsonify({
        "error": "Resource not found",
        "message": "The requested API endpoint does not exist."
    }), 404


@app.errorhandler(500)
def handle_server_error(error):

    print("Server error:", error)

    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server."
    }), 500


# ==========================================
# FILTER VALIDATION
# ==========================================

def get_filters():

    category = request.args.get(
        "category",
        ""
    ).strip()

    city = request.args.get(
        "city",
        ""
    ).strip()

    from_date = request.args.get(
        "from_date",
        ""
    ).strip()

    to_date = request.args.get(
        "to_date",
        ""
    ).strip()


    # --------------------------------------
    # Validate From Date
    # --------------------------------------

    if from_date:

        try:

            datetime.strptime(
                from_date,
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Invalid From Date. Use YYYY-MM-DD format."
            )


    # --------------------------------------
    # Validate To Date
    # --------------------------------------

    if to_date:

        try:

            datetime.strptime(
                to_date,
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Invalid To Date. Use YYYY-MM-DD format."
            )


    # --------------------------------------
    # Validate Date Range
    # --------------------------------------

    if from_date and to_date:

        if from_date > to_date:

            raise ValueError(
                "From Date cannot be later than To Date."
            )


    conditions = []

    parameters = []


    # --------------------------------------
    # Category Filter
    # --------------------------------------

    if category and category != "All":

        conditions.append(
            "p.Category = ?"
        )

        parameters.append(category)


    # --------------------------------------
    # City Filter
    # --------------------------------------

    if city and city != "All":

        conditions.append(
            "c.City = ?"
        )

        parameters.append(city)


    # --------------------------------------
    # From Date Filter
    # --------------------------------------

    if from_date:

        conditions.append(
            "o.OrderDate >= ?"
        )

        parameters.append(from_date)


    # --------------------------------------
    # To Date Filter
    # --------------------------------------

    if to_date:

        conditions.append(
            "o.OrderDate <= ?"
        )

        parameters.append(to_date)


    # --------------------------------------
    # Build WHERE Clause
    # --------------------------------------

    if conditions:

        where_clause = (
            "WHERE "
            + " AND ".join(conditions)
        )

    else:

        where_clause = ""


    return where_clause, parameters


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health")
def health_check():

    connection = None

    try:

        connection = get_db_connection()

        connection.execute(
            "SELECT 1"
        )

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })


    except sqlite3.Error as error:

        print(
            "Health check error:",
            error
        )

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 500


    finally:

        if connection:

            connection.close()


# ==========================================
# SUMMARY
# ==========================================

@app.route("/api/summary")
def summary():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            ROUND(
                COALESCE(
                    SUM(
                        o.Quantity * o.Price
                    ),
                    0
                ),
                2
            ) AS revenue,

            COUNT(
                DISTINCT o.OrderID
            ) AS orders,

            COUNT(
                DISTINCT o.CustomerID
            ) AS customers,

            ROUND(
                COALESCE(
                    AVG(
                        o.Quantity * o.Price
                    ),
                    0
                ),
                2
            ) AS average_order

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}
    """


    result = connection.execute(
        query,
        parameters
    ).fetchone()


    connection.close()


    return jsonify({

        "revenue": result["revenue"],

        "orders": result["orders"],

        "customers": result["customers"],

        "average_order":
            result["average_order"]

    })


# ==========================================
# MONTHLY SALES
# ==========================================

@app.route("/api/monthly-sales")
def monthly_sales():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            strftime(
                '%Y-%m',
                o.OrderDate
            ) AS month,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS revenue

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY month

        ORDER BY month
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "month": row["month"],
            "revenue": row["revenue"]
        }

        for row in data

    ])


# ==========================================
# CATEGORY SALES
# ==========================================

@app.route("/api/category-sales")
def category_sales():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            p.Category,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS revenue

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY p.Category

        ORDER BY revenue DESC
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "category": row["Category"],
            "revenue": row["revenue"]
        }

        for row in data

    ])


# ==========================================
# TOP PRODUCTS
# ==========================================

@app.route("/api/top-products")
def top_products():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            p.Product,

            SUM(
                o.Quantity
            ) AS quantity,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS revenue

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY p.Product

        ORDER BY revenue DESC

        LIMIT 10
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "product": row["Product"],
            "quantity": row["quantity"],
            "revenue": row["revenue"]
        }

        for row in data

    ])


# ==========================================
# TOP CUSTOMERS
# ==========================================

@app.route("/api/top-customers")
def top_customers():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            c.CustomerID,

            c.CustomerName,

            c.City,

            COUNT(
                o.OrderID
            ) AS orders,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS spending

        FROM customers c

        JOIN orders o
            ON c.CustomerID = o.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY

            c.CustomerID,

            c.CustomerName,

            c.City

        ORDER BY spending DESC

        LIMIT 10
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "customer_id": row["CustomerID"],
            "customer": row["CustomerName"],
            "city": row["City"],
            "orders": row["orders"],
            "spending": row["spending"]
        }

        for row in data

    ])


# ==========================================
# CITY SALES
# ==========================================

@app.route("/api/city-sales")
def city_sales():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            c.City,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS revenue

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY c.City

        ORDER BY revenue DESC
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "city": row["City"],
            "revenue": row["revenue"]
        }

        for row in data

    ])


# ==========================================
# PAYMENT METHODS
# ==========================================

@app.route("/api/payment-methods")
def payment_methods():

    where_clause, parameters = get_filters()

    connection = get_db_connection()


    query = f"""
        SELECT

            o.PaymentMethod,

            COUNT(
                o.OrderID
            ) AS orders,

            ROUND(
                SUM(
                    o.Quantity * o.Price
                ),
                2
            ) AS revenue

        FROM orders o

        JOIN customers c
            ON o.CustomerID = c.CustomerID

        JOIN products p
            ON o.ProductID = p.ProductID

        {where_clause}

        GROUP BY o.PaymentMethod

        ORDER BY revenue DESC
    """


    data = connection.execute(
        query,
        parameters
    ).fetchall()


    connection.close()


    return jsonify([

        {
            "method": row["PaymentMethod"],
            "orders": row["orders"],
            "revenue": row["revenue"]
        }

        for row in data

    ])


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )