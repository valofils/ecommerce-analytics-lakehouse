WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'raw_products') }}
),

cleaned AS (
    SELECT
        product_id,
        product_name,
        UPPER(TRIM(category)) AS category, -- Fix inconsistent casing
        -- Business Logic: If price is negative or 0, set to NULL (bad data)
        CASE 
            WHEN price <= 0 THEN NULL 
            ELSE price 
        END AS price,
        stock_quantity
    FROM source
)

SELECT * FROM cleaned