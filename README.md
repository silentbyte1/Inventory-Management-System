# Inventory Management System with Git Integration

## Overview
This is an inventory management system that uses SQLite for the database and Git for version control. The system allows:
- Store owners to manage products (add, update)
- Customers to make purchases
- All changes are tracked in Git history

## For Professor

### Assignment Submission
This submission includes:
- `inventory_manager.py` - The main Python file containing the complete application
- `README.md` - This documentation file
- When run, the program will generate `inventory_management.db` (SQLite database file)

### How to Run
1. Make sure Python is installed (Python 3.6 or higher recommended)
2. Run the single file application:
```
python inventory_manager.py
```
3. The application will:
   - Automatically create a SQLite database file (`inventory_management.db`)
   - Initialize a Git repository for version control
   - Ask if you want to add sample data for testing
   - Present a menu-driven interface to interact with the system

### Technical Choices
- **SQLite**: Used instead of MySQL for better portability (no server setup required)
- **Single-file Design**: All functionality is contained in one Python file for ease of evaluation
- **Automatic Dependency Installation**: Required packages will be installed automatically
- **Git Integration**: All inventory changes and purchases are recorded with Git commits

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

- All required Python packages will be installed automatically (gitpython, tabulate)
- The application is entirely contained in a single file for simplicity
- Git commits are used to track inventory changes and purchases

## Database Schema

The system uses the following tables:
- `products`: Store product information (name, price, quantity, category)
- `customers`: Store customer information (name, email, phone)
- `purchases`: Store purchase transactions (customer, total amount, date)
- `purchase_items`: Store individual items in each purchase (product, quantity, price)

## License

[MIT License](LICENSE)
