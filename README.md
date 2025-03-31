# Inventory Management System with Git Integration

## Overview
This is an inventory management system that uses MySQL for the database and Git for version control. The system allows:
- Store owners to manage products (add, update)
- Customers to make purchases
- All changes are tracked in Git history

## For Professor

### Assignment Submission
This submission includes:
- `inventory_manager.py` - The main Python file containing the complete application
- `README.md` - This documentation file
- The program connects to a MySQL database (and will create it if it doesn't exist)

### How to Run
1. Make sure Python is installed (Python 3.6 or higher recommended)
2. Make sure MySQL server is installed and running
3. Run the single file application:
```
python inventory_manager.py
```
4. The application will:
   - Prompt for MySQL connection details (host, username, password, database name)
   - Connect to your MySQL server and create the database if needed
   - Initialize a Git repository for version control
   - Ask if you want to add sample data for testing
   - Present a menu-driven interface to interact with the system

### MySQL Connection
When you start the program, you'll be prompted for:
- MySQL Host (default: localhost)
- MySQL Username (default: root) 
- MySQL Password
- Database Name (default: inventory_management)

The program will attempt to connect to your MySQL server with these credentials and create the database if it doesn't exist.

### Technical Choices
- **MySQL Database**: Used as requested in the assignment
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

- All required Python packages will be installed automatically (gitpython, tabulate, mysql-connector-python)
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
