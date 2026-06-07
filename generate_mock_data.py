import pandas as pd
import numpy as np
from faker import Faker
import os
import random

# Initialize Faker
fake = Faker()
Faker.seed(42) # For reproducibility

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

print("Generating Users...")
# ==========================================
# 1. USERS TABLE (Simulating a Postgres dump)
# ==========================================
num_users = 15_000
users = []
for i in range(1, num_users + 1):
    users.append({
        'user_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'created_at': fake.date_time_between(start_date='-3y', end_date='now'),
        # BAD DATA INJECTION: Some users have no country
        'country': fake.country_code() if random.random() > 0.05 else None 
    })

df_users = pd.DataFrame(users)

print("Generating Products...")
# ==========================================
# 2. PRODUCTS TABLE (Simulating a Postgres dump)
# ==========================================
num_products = 2_000
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Toys', 'Grocery', 'electronics', 'clothing'] # BAD DATA: Inconsistent casing
products = []
for i in range(1, num_products + 1):
    products.append({
        'product_id': i,
        'product_name': fake.catch_phrase(),
        'category': random.choice(categories),
        # BAD DATA INJECTION: Some prices are negative or zero
        'price': round(random.uniform(5.0, 500.0), 2) if random.random() > 0.02 else round(random.uniform(-50.0, 0.0), 2),
        'stock_quantity': random.randint(0, 1000)
    })

df_products = pd.DataFrame(products)

print("Generating Orders & Order Items...")
# ==========================================
# 3. ORDERS & ORDER ITEMS (Simulating Postgres dump)
# ==========================================
num_orders = 100_000
order_statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled', 'returned', 'shipped'] # BAD DATA: Inconsistent casing/statuses

orders = []
order_items = []
item_id_counter = 1

for order_id in range(1, num_orders + 1):
    user_id = random.randint(1, num_users)
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    status = random.choice(order_statuses)
    
    # BAD DATA INJECTION: Orphaned user_ids (rare, but happens in NoSQL/Dirty DBs)
    if random.random() < 0.01:
        user_id = 999999 
        
    orders.append({
        'order_id': order_id,
        'user_id': user_id,
        'status': status,
        'order_date': order_date
    })
    
    # Each order has 1 to 5 items
    num_items = random.randint(1, 5)
    items_in_order = random.sample(range(1, num_products + 1), num_items)
    
    for product_id in items_in_order:
        order_items.append({
            'order_item_id': item_id_counter,
            'order_id': order_id,
            'product_id': product_id,
            # BAD DATA INJECTION: Negative quantities
            'quantity': random.randint(1, 5) if random.random() > 0.03 else -1
        })
        item_id_counter += 1

df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)

# ==========================================
# 4. SAVE TO CSV (Simulating an S3/DB Export)
# ==========================================
print("Saving to CSV...")
df_users.to_csv('data/raw_users.csv', index=False)
df_products.to_csv('data/raw_products.csv', index=False)
df_orders.to_csv('data/raw_orders.csv', index=False)
df_order_items.to_csv('data/raw_order_items.csv', index=False)

print(f"Data generation complete! Generated {len(df_users)} users, {len(df_products)} products, {len(df_orders)} orders, and {len(df_order_items)} order items.")