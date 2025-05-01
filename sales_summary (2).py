
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_database():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    sample_data = [
        ('Apple', 10, 1.5),
        ('Banana', 20, 0.5),
        ('Apple', 5, 1.5),
        ('Orange', 15, 1.0),
        ('Banana', 10, 0.5),
        ('Orange', 5, 1.0)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

def query_database():
    conn = sqlite3.connect("sales_data.db")
    query = '''
        SELECT 
            product, 
            SUM(quantity) AS total_quantity, 
            SUM(quantity * price) AS revenue 
        FROM sales 
        GROUP BY product
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_results(df):
    print(df)
    df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("sales_chart.png")
    plt.show()

create_database()
df = query_database()
plot_results(df)
