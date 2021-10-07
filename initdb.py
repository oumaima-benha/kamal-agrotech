import sqlite3
import pandas as pd
products = pd.read_excel(
    'resources/db/test.xlsx', 
    sheet_name='Sheet1',
    header=0)
connection = sqlite3.connect("resources/db/products.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE products
    (Name TEXT, Category TEXT, Homologation TEXT, Composition TEXT, PackagingQuantity TEXT, PurchasePrice INTEGER, SellingPrice INTEGER, Quantity INTEGER)
""")
products.to_sql('products', connection, if_exists='append', index=False)

connection.commit()