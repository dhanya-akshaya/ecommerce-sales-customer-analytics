# E-Commerce Sales & Customer Analytics

A full-stack e-commerce analytics dashboard built using Python, Flask, SQLite, SQL, HTML, CSS, JavaScript, and Chart.js.

The application analyzes sales and customer data and presents the results through an interactive web dashboard.

---

## Project Overview

This project is designed to demonstrate how raw e-commerce transaction data can be converted into useful business insights.

The application provides:

- Sales performance analysis
- Customer spending analysis
- Product performance analysis
- Category-wise revenue analysis
- City-wise sales analysis
- Payment method analysis
- Monthly revenue trends
- Interactive filtering
- SQL-based analytics
- REST-style Flask APIs

The dataset used in this project is **synthetically generated for learning and demonstration purposes**.

---

## Features

### 1. KPI Dashboard

The dashboard displays:

- Total Revenue
- Total Orders
- Total Customers
- Average Order Value

---

### 2. Revenue Trend

A monthly revenue line chart shows how sales performance changes over time.

---

### 3. Category Analysis

A doughnut chart displays revenue distribution across product categories.

Categories include:

- Electronics
- Appliances
- Home
- Fashion
- Stationery
- Accessories

---

### 4. City-wise Sales

A bar chart compares revenue generated from different cities.

---

### 5. Payment Method Analysis

The dashboard analyzes orders based on payment methods such as:

- UPI
- Credit Card
- Debit Card
- Cash on Delivery
- Net Banking

---

### 6. Top Products

The application identifies the top 10 products based on revenue.

The table displays:

- Rank
- Product
- Quantity Sold
- Revenue

---

### 7. Top Customers

The application identifies the highest-value customers.

The table displays:

- Rank
- Customer
- City
- Number of Orders
- Total Spending

---

### 8. Interactive Filters

Users can filter dashboard results by:

- Category
- City
- From Date
- To Date

The dashboard updates its KPIs, charts, and tables based on the selected filters.

A Reset button restores the complete dataset.

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend

- Python
- Flask

### Database

- SQLite

### Data Analysis

- SQL
- SQL JOIN
- GROUP BY
- Aggregate Functions
- Common Table Expressions (CTEs)
- Window Functions
- RANK()
- LAG()

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## Project Architecture

```text
                    ┌─────────────────────┐
                    │     Web Browser     │
                    │  HTML/CSS/JavaScript│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    │      REST APIs      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     SQL Queries     │
                    │ JOIN / GROUP BY /   │
                    │ CTE / Window Funcs  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SQLite Database  │
                    │ Customers / Products│
                    │       / Orders      │
                    └─────────────────────┘