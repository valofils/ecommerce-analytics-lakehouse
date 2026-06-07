WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

users AS (
    SELECT * FROM {{ ref('stg_users') }}
),

joined AS (
    SELECT
        o.order_id,
        
        -- THE FIX: If the user_id from the order doesn't exist in the users table, map it to -1
        COALESCE(u.user_id, -1) AS user_id,
        
        o.status AS order_status,
        o.order_date,
        
        oi.order_item_id,
        oi.product_id,
        oi.quantity,
        
        p.price AS unit_price,
        
        -- Calculate item revenue. NULL prices/quantities will result in NULL revenue.
        (oi.quantity * p.price) AS item_revenue

    FROM orders o
    LEFT JOIN order_items oi 
        ON o.order_id = oi.order_id
    LEFT JOIN products p 
        ON oi.product_id = p.product_id
    LEFT JOIN users u 
        ON o.user_id = u.user_id  -- Added this join to check for user existence
)

SELECT * FROM joined