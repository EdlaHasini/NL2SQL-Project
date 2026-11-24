import sqlite3

def create_sample_db(db_path="ecommerce.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            signup_date DATE
        );
        
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            price REAL
        );
        
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)
    
    # Insert Sample Data
    cursor.executescript("""
        INSERT OR IGNORE INTO customers VALUES 
        (1, 'Alice Smith', 'alice@example.com', '2023-01-15'),
        (2, 'Bob Jones', 'bob@example.com', '2023-03-22');
        
        INSERT OR IGNORE INTO products VALUES 
        (101, 'Laptop', 'Electronics', 999.99),
        (102, 'Coffee Mug', 'Home', 15.50),
        (103, 'Desk Chair', 'Furniture', 150.00);
        
        INSERT OR IGNORE INTO orders VALUES 
        (1001, 1, 101, 1, '2023-05-10'),
        (1002, 1, 102, 2, '2023-06-15'),
        (1003, 2, 103, 1, '2023-07-01');
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database created at {db_path}")

if __name__ == "__main__":
    create_sample_db()