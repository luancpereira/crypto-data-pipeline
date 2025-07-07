CREATE OR REPLACE TABLE `cadastra-teste.APIcripto.assets_history` (
  id STRING,
  priceUsd FLOAT64,
  date DATE,
  hour STRING,
  execution_date DATE
)
PARTITION BY date;