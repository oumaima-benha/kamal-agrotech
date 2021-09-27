import sqlite3
connection = sqlite3.connect("resources/db/products.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE products
    (Name TEXT, Category TEXT, Homologation TEXT, Composition TEXT, PackagingQuantity TEXT, PurchasePrice INTEGER, SellingPrice INTEGER, Quantity INTEGER)
""")
cursor.execute("""INSERT INTO products VALUES 
    ('test', 'Herbicide', 'E02-7-009', 'elementx 10%', '1L', 22, 40, 100)
""")
connection.commit()