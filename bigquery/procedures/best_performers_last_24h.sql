CREATE OR REPLACE PROCEDURE `cadastra-teste.APIcripto.best_performers_last_24h`()
BEGIN

  CREATE OR REPLACE TABLE `cadastra-teste.APIcripto_gold.best_performers_last_24h` AS (

    WITH latest_assets AS (
      SELECT *
      FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC, priceUsd DESC) AS rn
        FROM `cadastra-teste.APIcripto.assets`
        WHERE date = CURRENT_DATE()
          AND changePercent24Hr IS NOT NULL
          AND marketCapUsd > 1000000
      )
      WHERE rn = 1
    ),

    best_performers AS (
      SELECT 
        'up' AS category,
        name,
        symbol,
        priceUsd,
        changePercent24Hr / 100 AS changePercent24Hr,
        marketCapUsd,
        volumeUsd24Hr,
        RANK() OVER (ORDER BY changePercent24Hr DESC) AS ranking,
        CURRENT_DATETIME() AS last_updated
      FROM latest_assets
      ORDER BY changePercent24Hr DESC
      LIMIT 10
    ),

    worst_performers AS (
      SELECT 
        'down' AS category,
        name,
        symbol,
        priceUsd,
        changePercent24Hr / 100 AS changePercent24Hr,
        marketCapUsd,
        volumeUsd24Hr,
        RANK() OVER (ORDER BY changePercent24Hr ASC) AS ranking,
        CURRENT_DATETIME() AS last_updated
      FROM latest_assets
      ORDER BY changePercent24Hr ASC
      LIMIT 10
    )

    SELECT * FROM best_performers
    UNION ALL
    SELECT * FROM worst_performers

  );

END;