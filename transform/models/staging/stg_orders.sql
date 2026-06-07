WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'raw_orders') }}
),

cleaned AS (
    SELECT
        order_id,
        user_id,
        UPPER(TRIM(status)) AS status, -- Fix inconsistent casing (e.g., 'shipped' -> 'SHIPPED')
        order_date
    FROM source
    -- Data Quality: Filter out orders with null order_id or null order_date
    WHERE order_id IS NOT NULL 
      AND order_date IS NOT NULL
)

SELECT * FROM cleaned