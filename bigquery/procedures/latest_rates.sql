CREATE OR REPLACE PROCEDURE `cadastra-teste.APIcripto.latest_rates`()
BEGIN 
  CREATE OR REPLACE TABLE `cadastra-teste.APIcripto_gold.latest_rates` AS
  (
    WITH latest_rates AS (
      SELECT 
        id,
        rateUsd,
        date,
        hour,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY date DESC, hour DESC) as rn
      FROM `cadastra-teste.APIcripto.rates`
    )
    SELECT 
      id,
      rateUsd,
      date,
      hour
    FROM latest_rates
    WHERE rn = 1
    ORDER BY id
  );
END;