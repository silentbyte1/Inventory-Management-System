# Inventory Management System with Git Integration

## Overview
This is an inventory management system that uses SQLite for the database and Git for version control. The system allows:
- Store owners to manage products (add, update)
- Customers to make purchases
- All changes are tracked in Git history

## How to Run

1. Make sure you have Python installed (Python 3.6 or higher recommended)

2. Run the single file application:
```
python inventory_manager.py
```

3. The application will:
   - Automatically create a SQLite database file (`inventory_management.db`)
   - Initialize a Git repository for version control
   - Ask if you want to add sample data for testing
   - Present a menu-driven interface to interact with the system

## Files Included

- `inventory_manager.py` - The main executable Python file
- `inventory_management.db` - SQLite database file (created when you run the program)
- `.git/` - Git repository directory (created when you run the program)

## Features

1. **Product Management**
   - View all products
   - Add new products
   - Update existing products

2. **Customer Management**
   - View all customers
   - Add new customers

3. **Purchase Processing**
   - Select customer
   - Add products to cart
   - Complete purchase with automatic inventory update

4. **History Tracking**
   - Database purchase history
   - Git-based purchase history

## Technical Details

- The program uses SQLite for the database instead of MySQL for portability
- All required Python packages will be installed automatically (gitpython, tabulate)
- The application is entirely contained in a single file for simplicity
- Git commits are used to track inventory changes and purchases

## Database Schema

The system uses the following tables:
- `products`: Store product information (name, price, quantity, category)
- `customers`: Store customer information (name, email, phone)
- `purchases`: Store purchase transactions (customer, total amount, date)
- `purchase_items`: Store individual items in each purchase (product, quantity, price) 