import os
import sys
import time
from datetime import datetime
from tabulate import tabulate

# Check if required packages are installed, if not install them
try:
    import git
    import mysql.connector
except ImportError:
    print("Installing required packages...")
    import subprocess
    packages = ["gitpython", "tabulate", "mysql-connector-python"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    import git
    import mysql.connector
    from tabulate import tabulate

# Database setup
class Database:
    def __init__(self, host="localhost", user="root", password="", database="inventory_management"):
        self.host = host
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()
        
    def connect(self):
        """Connect to MySQL database"""
        try:
            # First connect without database to create it if needed
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            
            # Create database if it doesn't exist
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.cursor.execute(f"USE {self.database}")
            
            # Create tables if they don't exist
            self._create_tables()
            
            print(f"Connected to MySQL database: {self.database}")
            return True
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        tables = {}
        
        # Products table
        tables['products'] = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Customers table
        tables['customers'] = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Purchases table
        tables['purchases'] = """
        CREATE TABLE IF NOT EXISTS purchases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            total_amount DECIMAL(10, 2) NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL
        )
        """
        
        # Purchase items table
        tables['purchase_items'] = """
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            purchase_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price_per_unit DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """
        
        for table_name, query in tables.items():
            try:
                self.cursor.execute(query)
                print(f"Created table {table_name} if it didn't exist")
            except mysql.connector.Error as e:
                print(f"Error creating table {table_name}: {e}")
    
    def execute_query(self, query, params=None):
        """Execute a query with optional parameters"""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return False
    
    def fetch_all(self, query, params=None):
        """Execute a query and fetch all results"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Execute a query and fetch one result"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")

# Git Manager
class GitManager:
    def __init__(self, repo_path='.'):
        """Initialize git manager with repo path"""
        self.repo_path = repo_path
        self.setup_repo()
    
    def setup_repo(self):
        """Setup git repository if it doesn't exist"""
        try:
            self.repo = git.Repo(self.repo_path)
            print("Git repository already exists")
        except git.exc.InvalidGitRepositoryError:
            print("Initializing new git repository")
            self.repo = git.Repo.init(self.repo_path)
    
    def commit_changes(self, message):
        """Commit all changes with the provided message"""
        try:
            # Add all changes
            self.repo.git.add('--all')
            
            # Check if there are changes to commit
            if self.repo.is_dirty() or len(self.repo.untracked_files) > 0:
                self.repo.git.commit('-m', message)
                print(f"Changes committed: {message}")
                return True
            else:
                print("No changes to commit")
                return False
        except Exception as e:
            print(f"Error committing changes: {e}")
            return False
    
    def record_purchase(self, customer_name, products):
        """Record a purchase in git history
        
        Args:
            customer_name (str): Name of the customer
            products (list): List of tuples (product_name, quantity, price)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Purchase: {customer_name} - {timestamp}\n\n"
        
        for product_name, quantity, price in products:
            message += f"* {product_name} x{quantity} @ ${price:.2f}\n"
        
        return self.commit_changes(message)
    
    def record_inventory_update(self, updated_products):
        """Record inventory updates in git history
        
        Args:
            updated_products (list): List of tuples (product_name, old_qty, new_qty)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Inventory Update: {timestamp}\n\n"
        
        for product_name, old_qty, new_qty in updated_products:
            message += f"* {product_name}: {old_qty} → {new_qty}\n"
        
        return self.commit_changes(message)
    
    def get_purchase_history(self, limit=10):
        """Get purchase history from git logs
        
        Args:
            limit (int): Maximum number of history entries to return
        
        Returns:
            list: List of commit messages related to purchases
        """
        history = []
        
        try:
            for commit in list(self.repo.iter_commits())[:limit]:
                if commit.message.startswith("Purchase:"):
                    history.append(commit.message)
        except Exception as e:
            print(f"Error getting purchase history: {e}")
        
        return history

# Models
class Product:
    def __init__(self, db):
        self.db = db
    
    def add_product(self, name, price, quantity, category=None):
        """Add a new product to the inventory"""
        query = """
        INSERT INTO products (name, price, quantity, category)
        VALUES (%s, %s, %s, %s)
        """
        params = (name, price, quantity, category)
        return self.db.execute_query(query, params)
    
    def update_product(self, product_id, name=None, price=None, quantity=None, category=None):
        """Update an existing product"""
        # Get the current product data
        current = self.get_product_by_id(product_id)
        if not current:
            return False
        
        # Use current values if new ones are not provided
        name = name if name is not None else current[1]
        price = price if price is not None else current[2]
        quantity = quantity if quantity is not None else current[3]
        category = category if category is not None else current[4]
        
        query = """
        UPDATE products
        SET name = %s, price = %s, quantity = %s, category = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        params = (name, price, quantity, category, product_id)
        return self.db.execute_query(query, params)
    
    def get_all_products(self):
        """Get all products"""
        query = "SELECT * FROM products ORDER BY name"
        return self.db.fetch_all(query)
    
    def get_product_by_id(self, product_id):
        """Get a product by its ID"""
        query = "SELECT * FROM products WHERE id = %s"
        return self.db.fetch_one(query, (product_id,))
    
    def get_product_by_name(self, name):
        """Get a product by its name"""
        query = "SELECT * FROM products WHERE name = %s"
        return self.db.fetch_one(query, (name,))
    
    def update_quantity(self, product_id, quantity_change):
        """Update product quantity (positive = add, negative = remove)"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        
        current_quantity = product[3]
        new_quantity = current_quantity + quantity_change
        
        if new_quantity < 0:
            print(f"Error: Insufficient quantity for product #{product_id}")
            return False
        
        query = "UPDATE products SET quantity = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        params = (new_quantity, product_id)
        return self.db.execute_query(query, params)

class Customer:
    def __init__(self, db):
        self.db = db
    
    def add_customer(self, name, email=None, phone=None):
        """Add a new customer"""
        query = """
        INSERT INTO customers (name, email, phone)
        VALUES (%s, %s, %s)
        """
        params = (name, email, phone)
        return self.db.execute_query(query, params)
    
    def get_all_customers(self):
        """Get all customers"""
        query = "SELECT * FROM customers ORDER BY name"
        return self.db.fetch_all(query)
    
    def get_customer_by_id(self, customer_id):
        """Get a customer by ID"""
        query = "SELECT * FROM customers WHERE id = %s"
        return self.db.fetch_one(query, (customer_id,))
    
    def get_customer_by_email(self, email):
        """Get a customer by email"""
        query = "SELECT * FROM customers WHERE email = %s"
        return self.db.fetch_one(query, (email,))

class Purchase:
    def __init__(self, db):
        self.db = db
    
    def create_purchase(self, customer_id, items):
        """Create a new purchase
        
        Args:
            customer_id (int): ID of the customer
            items (list): List of tuples (product_id, quantity)
        
        Returns:
            tuple: (success, purchase_id, items_details)
        """
        product_model = Product(self.db)
        total_amount = 0
        items_details = []
        
        # Calculate total and verify quantities
        for product_id, quantity in items:
            product = product_model.get_product_by_id(product_id)
            if not product:
                print(f"Error: Product #{product_id} not found")
                return False, None, None
            
            if product[3] < quantity:
                print(f"Error: Insufficient quantity for {product[1]}")
                return False, None, None
            
            item_total = product[2] * quantity
            total_amount += item_total
            
            # Store details for later use
            items_details.append((product[0], product[1], quantity, product[2]))
        
        # Create purchase record
        query = """
        INSERT INTO purchases (customer_id, total_amount)
        VALUES (%s, %s)
        """
        params = (customer_id, total_amount)
        if not self.db.execute_query(query, params):
            return False, None, None
        
        # Get the purchase ID - modified for MySQL
        self.db.cursor.execute("SELECT LAST_INSERT_ID()")
        purchase_id = self.db.cursor.fetchone()[0]
        
        # Add purchase items
        for product_id, product_name, quantity, price in items_details:
            query = """
            INSERT INTO purchase_items (purchase_id, product_id, quantity, price_per_unit)
            VALUES (%s, %s, %s, %s)
            """
            params = (purchase_id, product_id, quantity, price)
            if not self.db.execute_query(query, params):
                print(f"Error adding purchase item for {product_name}")
            
            # Update product quantity
            product_model.update_quantity(product_id, -quantity)
        
        return True, purchase_id, items_details
    
    def get_purchase_by_id(self, purchase_id):
        """Get purchase details by ID"""
        query = """
        SELECT p.id, p.customer_id, p.total_amount, p.purchase_date, c.name
        FROM purchases p
        LEFT JOIN customers c ON p.customer_id = c.id
        WHERE p.id = %s
        """
        return self.db.fetch_one(query, (purchase_id,))
    
    def get_purchase_items(self, purchase_id):
        """Get all items in a purchase"""
        query = """
        SELECT pi.id, pi.product_id, pi.quantity, pi.price_per_unit, p.name
        FROM purchase_items pi
        JOIN products p ON pi.product_id = p.id
        WHERE pi.purchase_id = %s
        """
        return self.db.fetch_all(query, (purchase_id,))
    
    def get_all_purchases(self, limit=50):
        """Get all purchases"""
        query = """
        SELECT p.id, p.customer_id, p.total_amount, p.purchase_date, c.name
        FROM purchases p
        LEFT JOIN customers c ON p.customer_id = c.id
        ORDER BY p.purchase_date DESC
        LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

# Main Application
class InventoryApp:
    def __init__(self):
        # Prompt for database connection settings
        print("\n=== Database Connection Settings ===")
        print("(Press Enter to use defaults)")
        host = input("MySQL Host [localhost]: ") or "localhost"
        user = input("MySQL Username [root]: ") or "root"
        password = input("MySQL Password: ") or ""
        database = input("Database Name [inventory_management]: ") or "inventory_management"
        
        self.db = Database(host, user, password, database)
        self.git = GitManager()
        self.product_model = Product(self.db)
        self.customer_model = Customer(self.db)
        self.purchase_model = Purchase(self.db)
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu"""
        self.clear_screen()
        print("=" * 50)
        print("           INVENTORY MANAGEMENT SYSTEM           ")
        print("=" * 50)
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. View Customers")
        print("5. Add Customer")
        print("6. Make Purchase")
        print("7. View Purchase History")
        print("8. View Git Purchase History")
        print("9. Exit")
        print("=" * 50)
    
    def view_products(self):
        """View all products"""
        products = self.product_model.get_all_products()
        
        if not products:
            print("\nNo products found in inventory.")
            return
        
        headers = ["ID", "Name", "Price", "Quantity", "Category", "Created At", "Updated At"]
        print("\n" + tabulate(products, headers=headers, tablefmt="grid"))
    
    def add_product(self):
        """Add a new product"""
        print("\n=== Add New Product ===")
        name = input("Enter product name: ")
        
        if not name:
            print("Product name cannot be empty.")
            return
        
        # Check if product already exists
        existing = self.product_model.get_product_by_name(name)
        if existing:
            print(f"A product with name '{name}' already exists.")
            return
        
        try:
            price = float(input("Enter price: $"))
            quantity = int(input("Enter quantity: "))
            category = input("Enter category (optional): ") or None
        except ValueError:
            print("Invalid input. Price must be a number and quantity must be an integer.")
            return
        
        if self.product_model.add_product(name, price, quantity, category):
            print(f"\nProduct '{name}' added successfully.")
            
            # Record in git
            self.git.record_inventory_update([(name, 0, quantity)])
        else:
            print("Failed to add product.")
    
    def update_product(self):
        """Update an existing product"""
        self.view_products()
        
        try:
            product_id = int(input("\nEnter product ID to update: "))
        except ValueError:
            print("Invalid input. ID must be an integer.")
            return
        
        product = self.product_model.get_product_by_id(product_id)
        if not product:
            print(f"No product found with ID {product_id}.")
            return
        
        print(f"\nUpdating product: {product[1]}")
        print("(Press Enter to keep current value)")
        
        name = input(f"Name [{product[1]}]: ") or None
        price_str = input(f"Price [${product[2]}]: ") or None
        quantity_str = input(f"Quantity [{product[3]}]: ") or None
        category = input(f"Category [{product[4] or 'None'}]: ") or None
        
        try:
            price = float(price_str) if price_str else None
            quantity = int(quantity_str) if quantity_str else None
        except ValueError:
            print("Invalid input. Price must be a number and quantity must be an integer.")
            return
        
        old_quantity = product[3]
        
        if self.product_model.update_product(product_id, name, price, quantity, category):
            print(f"\nProduct #{product_id} updated successfully.")
            
            # Record in git if quantity changed
            if quantity is not None and quantity != old_quantity:
                product_name = name or product[1]
                self.git.record_inventory_update([(product_name, old_quantity, quantity)])
        else:
            print("Failed to update product.")
    
    def view_customers(self):
        """View all customers"""
        customers = self.customer_model.get_all_customers()
        
        if not customers:
            print("\nNo customers found.")
            return
        
        headers = ["ID", "Name", "Email", "Phone", "Created At"]
        print("\n" + tabulate(customers, headers=headers, tablefmt="grid"))
    
    def add_customer(self):
        """Add a new customer"""
        print("\n=== Add New Customer ===")
        name = input("Enter customer name: ")
        
        if not name:
            print("Customer name cannot be empty.")
            return
        
        email = input("Enter email (optional): ") or None
        phone = input("Enter phone (optional): ") or None
        
        if email:
            existing = self.customer_model.get_customer_by_email(email)
            if existing:
                print(f"A customer with email '{email}' already exists.")
                return
        
        if self.customer_model.add_customer(name, email, phone):
            print(f"\nCustomer '{name}' added successfully.")
        else:
            print("Failed to add customer.")
    
    def make_purchase(self):
        """Make a new purchase"""
        # Select customer
        self.view_customers()
        
        try:
            customer_id = int(input("\nEnter customer ID (0 for anonymous): "))
            if customer_id != 0:
                customer = self.customer_model.get_customer_by_id(customer_id)
                if not customer:
                    print(f"No customer found with ID {customer_id}.")
                    return
                customer_name = customer[1]
            else:
                customer_id = None
                customer_name = "Anonymous"
        except ValueError:
            print("Invalid input. ID must be an integer.")
            return
        
        # Add products to purchase
        self.view_products()
        items = []
        product_details = []
        
        print("\n=== Add Products to Purchase ===")
        print("(Enter 0 for product ID to finish)")
        
        while True:
            try:
                product_id = int(input("\nEnter product ID: "))
                if product_id == 0:
                    break
                
                product = self.product_model.get_product_by_id(product_id)
                if not product:
                    print(f"No product found with ID {product_id}.")
                    continue
                
                quantity = int(input(f"Enter quantity for {product[1]} (available: {product[3]}): "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    continue
                
                if quantity > product[3]:
                    print(f"Error: Only {product[3]} units available.")
                    continue
                
                items.append((product_id, quantity))
                product_details.append((product[1], quantity, product[2]))
                print(f"Added {quantity} x {product[1]} to cart.")
            except ValueError:
                print("Invalid input. ID and quantity must be integers.")
        
        if not items:
            print("Purchase cancelled - no items selected.")
            return
        
        # Process purchase
        success, purchase_id, items_details = self.purchase_model.create_purchase(customer_id, items)
        
        if success:
            print(f"\nPurchase completed successfully! Purchase ID: {purchase_id}")
            
            # Record in git
            self.git.record_purchase(customer_name, product_details)
        else:
            print("Purchase failed.")
    
    def view_purchase_history(self):
        """View purchase history from database"""
        purchases = self.purchase_model.get_all_purchases()
        
        if not purchases:
            print("\nNo purchase history found.")
            return
        
        headers = ["ID", "Customer ID", "Total Amount", "Purchase Date", "Customer Name"]
        print("\n" + tabulate(purchases, headers=headers, tablefmt="grid"))
        
        try:
            purchase_id = int(input("\nEnter purchase ID to view details (0 to cancel): "))
            if purchase_id == 0:
                return
            
            items = self.purchase_model.get_purchase_items(purchase_id)
            if not items:
                print(f"No items found for purchase #{purchase_id}.")
                return
            
            headers = ["ID", "Product ID", "Quantity", "Price Per Unit", "Product Name"]
            print("\n" + tabulate(items, headers=headers, tablefmt="grid"))
        except ValueError:
            print("Invalid input. ID must be an integer.")
    
    def view_git_history(self):
        """View purchase history from git"""
        history = self.git.get_purchase_history()
        
        if not history:
            print("\nNo git purchase history found.")
            return
        
        for i, commit in enumerate(history, 1):
            print(f"\n{i}. {commit}")
    
    def add_sample_data(self):
        """Add sample data for demonstration"""
        print("\nAdding sample data for demonstration...")
        
        # Add sample products
        products = [
            ("Laptop", 999.99, 10, "Electronics"),
            ("Smartphone", 599.99, 20, "Electronics"),
            ("Headphones", 89.99, 30, "Accessories"),
            ("Mouse", 24.99, 50, "Accessories"),
            ("Keyboard", 49.99, 40, "Accessories"),
            ("Monitor", 299.99, 15, "Electronics"),
            ("USB Drive", 19.99, 100, "Storage"),
            ("External HDD", 79.99, 25, "Storage")
        ]
        
        for name, price, quantity, category in products:
            if not self.product_model.get_product_by_name(name):
                self.product_model.add_product(name, price, quantity, category)
                print(f"Added product: {name}")
        
        # Add sample customers
        customers = [
            ("John Smith", "john@example.com", "555-1234"),
            ("Jane Doe", "jane@example.com", "555-5678"),
            ("Bob Johnson", "bob@example.com", "555-9012")
        ]
        
        for name, email, phone in customers:
            if not self.customer_model.get_customer_by_email(email):
                self.customer_model.add_customer(name, email, phone)
                print(f"Added customer: {name}")
        
        # Record in git
        self.git.record_inventory_update([("Sample Data", 0, 1)])
        print("\nSample data added successfully!")
    
    def run(self):
        """Run the application"""
        print("\nWelcome to the Inventory Management System!")
        print("Connected to MySQL database")
        print("The application will initialize a Git repository for version control.\n")
        
        # Ask if user wants sample data
        sample_data = input("Would you like to add sample data for demonstration? (y/n): ")
        if sample_data.lower() == 'y':
            self.add_sample_data()
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == '1':
                self.view_products()
            elif choice == '2':
                self.add_product()
            elif choice == '3':
                self.update_product()
            elif choice == '4':
                self.view_customers()
            elif choice == '5':
                self.add_customer()
            elif choice == '6':
                self.make_purchase()
            elif choice == '7':
                self.view_purchase_history()
            elif choice == '8':
                self.view_git_history()
            elif choice == '9':
                self.db.close()
                print("\nExiting Inventory Management System. Goodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = InventoryApp()
    app.run() 