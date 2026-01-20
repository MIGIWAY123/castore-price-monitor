import sqlite3

conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# Считаем уникальные товары
cursor.execute("SELECT count(*) FROM products")
products_count = cursor.fetchone()[0]

# Считаем общее количество записей цен
cursor.execute("SELECT count(*) FROM price_history")
prices_count = cursor.fetchone()[0]

print(f"✅ В базе данных {products_count} уникальных товаров.")
print(f"📈 Всего записей в истории цен: {prices_count}.")

conn.close()