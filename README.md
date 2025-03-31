# Inventory Management System

A Python-based inventory management system with Git integration for version control and purchase history tracking.

## Features

- **Product Management**: Add, view, and update products in inventory
- **Customer Management**: Add and view customers
- **Purchase System**: Process purchases with automatic inventory updates
- **Git Integration**: All inventory updates and purchases are recorded in Git history
- **MySQL Database**: Persistent storage of inventory, customers, and purchases

## Prerequisites

- Python 3.6 or higher
- MySQL Server
- Git

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd inventory-management
```

2. Install required Python packages:
```
pip install -r requirements.txt
```

3. Configure database connection:
Edit the `.env` file with your MySQL database credentials:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=inventory_management
```

## Usage

Run the application:
```
python inventory_app.py
```

### Main Menu Options:

1. **View Products**: Display all products in inventory
2. **Add Product**: Add a new product to inventory
3. **Update Product**: Update an existing product (name, price, quantity, category)
4. **View Customers**: Display all registered customers
5. **Add Customer**: Register a new customer
6. **Make Purchase**: Process a new purchase with automatic inventory updates
7. **View Purchase History**: View purchase history from the database
8. **View Git Purchase History**: View purchase history from Git commits
9. **Exit**: Exit the application

## Database Schema

The system uses the following tables:

- **products**: Store product information (name, price, quantity, category)
- **customers**: Store customer information (name, email, phone)
- **purchases**: Store purchase transactions (customer, total amount, date)
- **purchase_items**: Store individual items in each purchase (product, quantity, price)

## Git Integration

All inventory changes and purchases are automatically committed to Git with descriptive messages:

- Product additions/updates: "Inventory Update: [timestamp]"
- Purchases: "Purchase: [customer] - [timestamp]"

## License

[MIT License](LICENSE)
