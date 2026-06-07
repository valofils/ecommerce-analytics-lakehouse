WITH source AS (
    SELECT * FROM {{ source('raw_ecommerce', 'raw_users') }}
),

cleaned AS (
    SELECT
        user_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        LOWER(email) AS email, -- Standardize emails to lowercase
        created_at,
        COALESCE(country, 'Unknown') AS country -- Handle missing countries
    FROM source
    WHERE user_id IS NOT NULL -- Remove any completely null rows
)

SELECT * FROM cleaned