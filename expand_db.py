import sqlite3

def expand():
    conn = sqlite3.connect("ecommerce.db"); cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS employees (employee_id INTEGER PRIMARY KEY, name TEXT, role TEXT, hire_date DATE);
    CREATE TABLE IF NOT EXISTS stores (store_id INTEGER PRIMARY KEY, store_name TEXT, city TEXT);
    CREATE TABLE IF NOT EXISTS shipments (shipment_id INTEGER PRIMARY KEY, order_id INTEGER, ship_date DATE, status TEXT);
    CREATE TABLE IF NOT EXISTS payments (payment_id INTEGER PRIMARY KEY, order_id INTEGER, amount REAL, method TEXT, paid_date DATE);
    CREATE TABLE IF NOT EXISTS reviews (review_id INTEGER PRIMARY KEY, product_id INTEGER, customer_id INTEGER, rating INTEGER, review_text TEXT);
    CREATE TABLE IF NOT EXISTS suppliers (supplier_id INTEGER PRIMARY KEY, supplier_name TEXT, country TEXT);

    INSERT OR IGNORE INTO employees VALUES (1,'Priya Sharma','Manager','2022-05-01'),(2,'Rahul Verma','Cashier','2023-02-10');
    INSERT OR IGNORE INTO stores VALUES (1,'Downtown Store','Mumbai'),(2,'Airport Store','Delhi');
    INSERT OR IGNORE INTO shipments VALUES (1,1001,'2023-05-12','delivered'),(2,1002,'2023-06-17','delivered'),(3,1003,'2023-07-03','in_transit');
    INSERT OR IGNORE INTO payments VALUES (1,1001,999.99,'card','2023-05-10'),(2,1002,31.00,'upi','2023-06-15'),(3,1003,150.00,'card','2023-07-01');
    INSERT OR IGNORE INTO reviews VALUES (1,101,1,5,'Great laptop!'),(2,102,1,4,'Nice mug'),(3,103,2,4,'Comfy chair');
    INSERT OR IGNORE INTO suppliers VALUES (1,'TechCorp','China'),(2,'HomeGoods Ltd','India');
    """)
    conn.commit(); conn.close()
    print("✅ Database expanded to 9 tables")

if __name__ == "__main__":
    expand()