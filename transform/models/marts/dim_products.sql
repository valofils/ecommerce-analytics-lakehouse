WITH source AS (
    SELECT * FROM {{ ref('stg_products') }}
),

final AS (
    SELECT
        product_id,
        product_name,
        category,
        price AS current_price, -- Renaming for business clarity
        stock_quantity
    FROM source
)

SELECT * FROM final