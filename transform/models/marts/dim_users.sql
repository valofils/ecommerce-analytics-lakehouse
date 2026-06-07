WITH source AS (
    SELECT * FROM {{ ref('stg_users') }}
),

final AS (
    SELECT
        user_id,
        first_name,
        last_name,
        email,
        country,
        created_at AS user_created_at
    FROM source

    UNION ALL

    -- Catch-all row for orphaned transactions to maintain referential integrity
    SELECT
        -1 AS user_id,
        'Unknown' AS first_name,
        'Unknown' AS last_name,
        'unknown@unknown.com' AS email,
        'Unknown' AS country,
        CAST('1900-01-01' AS TIMESTAMP) AS user_created_at
)

SELECT * FROM final