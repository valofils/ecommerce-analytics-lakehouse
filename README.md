# 🛒 E-Commerce Analytics Lakehouse

An end-to-end ELT (Extract, Load, Transform) data pipeline simulating an Amazon-style e-commerce marketplace. This project processes **300k+ records** from a simulated transactional database, cleans data anomalies, and models them into a **Kimball-style Star Schema** for analytics.

---

# 🏗️ Architecture & Tech Stack

* **Language:** Python, SQL
* **Data Warehouse:** DuckDB (Local, high-performance analytical database)
* **Transformation:** dbt (Data Build Tool)
* **Data Modeling:** Star Schema (Kimball Methodology)

---

# 🧠 Business Context & Engineering Decisions

In real-world e-commerce systems, raw data is messy. This pipeline is specifically designed to handle common data engineering challenges:

## Data Quality Enforcement

Handled negative product prices and order quantities by neutralizing them to `NULL` during the staging layer, preventing them from skewing financial metrics.

## Categorical Standardization

Cleaned inconsistent casing (e.g., `'Shipped'` vs `'shipped'`) by applying `UPPER()` and `TRIM()` to standardize statuses and categories.

## Referential Integrity Resolution

Discovered ~3,000 orphaned orders (orders with a `user_id` that doesn't exist in the users table). Instead of deleting valuable revenue data, I created a **"Catch-All" dimension record** (`user_id = -1`, `"Unknown User"`) and used `COALESCE` to map orphaned transactions, ensuring BI dashboards don't break.

---

# 📊 Data Model (Star Schema)

## dbt Lineage Graph

### `dim_users`

Cleaned user data, including the catch-all `"Unknown"` user.

### `dim_products`

Product catalog with standardized categories.

### `fct_order_items`

The central fact table containing order events, quantities, and calculated `item_revenue`.

---

# 🔬 Data Quality Testing

Data trust is paramount. Using dbt, I implemented **10 automated tests** to ensure pipeline reliability:

* **Uniqueness & Non-Null**

  * Primary keys on all `user_id`, `product_id`, and `order_item_id`.

* **Accepted Values**

  * Ensured `order_status` and `category` only contain approved, standardized values.

* **Relationships**

  * Verified that every `user_id` and `product_id` in the fact table exists in its respective dimension table.

---

# 📈 Project Evolution

✅ **Incremental Models:** Implemented an incremental `delete+insert` strategy on `fct_order_items` using the `is_incremental()` macro to optimize pipeline runtimes for new daily data.

✅ **BI Layer:** Built an interactive Streamlit dashboard to visualize Monthly Revenue Trends, Category Performance, and core KPIs (AOV, Total Revenue).

---

# 🚀 How to Run This Project

## Prerequisites

* Python 3.8+

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-analytics-lakehouse.git
cd ecommerce-analytics-lakehouse
```

---

## 2. Set Up the Environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

## 3. Generate the Mock Raw Data

```bash
python generate_mock_data.py
```

---

## 4. Load Data into the Data Warehouse

```bash
python load_to_duckdb.py
```

---

## 5. Run the dbt Transformation Pipeline

```bash
cd transform
dbt run
```

---

## 6. Run the Data Quality Tests

```bash
dbt test
```

---

## 7. Launch the Streamlit Dashboard

```bash
streamlit run dashboard.py
```
