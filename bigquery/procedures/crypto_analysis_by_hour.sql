CREATE OR REPLACE PROCEDURE `cadastra-teste.APIcripto.crypto_analysis_by_hour`()
BEGIN
  DECLARE max_execution_date DATE;
  DECLARE target_date DATE;

  CREATE TABLE IF NOT EXISTS `cadastra-teste.APIcripto_gold.crypto_analysis_by_hour` (
    crypto_id STRING,
    current_price FLOAT64,
    date DATE,
    hour STRING,
    execution_date DATE,
    pct_change_1h FLOAT64,
    daily_high FLOAT64,
    daily_low FLOAT64,
    processed_at TIMESTAMP
  );
  
  SET max_execution_date = (
    SELECT MAX(execution_date) 
    FROM `cadastra-teste.APIcripto_gold.crypto_analysis_by_hour`
  );
  
  IF max_execution_date IS NULL THEN
    SET max_execution_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);
  END IF;
  
  SET target_date = max_execution_date;
  
  IF target_date >= CURRENT_DATE() THEN
    RETURN;
  END IF;

  INSERT INTO `cadastra-teste.APIcripto_gold.crypto_analysis_by_hour`
  SELECT 
    id as crypto_id,
    priceUsd as current_price,
    date,
    hour,
    execution_date,
    
    CASE 
      WHEN LAG(priceUsd, 1) OVER (PARTITION BY id ORDER BY date, hour) IS NOT NULL THEN 
        ROUND((priceUsd - LAG(priceUsd, 1) OVER (PARTITION BY id ORDER BY date, hour)) / 
              LAG(priceUsd, 1) OVER (PARTITION BY id ORDER BY date, hour) * 100, 4)
      ELSE NULL 
    END as pct_change_1h,
    
    MAX(priceUsd) OVER (PARTITION BY id, date) as daily_high,
    MIN(priceUsd) OVER (PARTITION BY id, date) as daily_low,
    
    CURRENT_TIMESTAMP() as processed_at
    
  FROM `cadastra-teste.APIcripto.assets_history`
  WHERE date = target_date;

END;
