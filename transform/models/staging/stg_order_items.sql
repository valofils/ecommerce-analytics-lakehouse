WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'raw_order_items') }}
),

cleaned AS (
    SELECT
        order_item_id,
        order_id,
        product_id,
        -- Business Logic: If quantity is negative, set to NULL (bad data)
        CASE 
            WHEN quantity <= 0 THEN NULL 
            ELSE quantity 
        END AS quantity
    FROM source
)

SELECT * FROM cleaned