import sqlite3
connection = sqlite3.connect("products.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE products
    (id INTEGER, name TEXT, description TEXT,experiation_date Date, price INTEGER, quantity INTEGER)
""")
cursor.execute("""INSERT INTO products VALUES 
    (1, 'tid', 'mas7ou9 jmil', '1970-01-01', 12, 100)
""")
connection.commit()