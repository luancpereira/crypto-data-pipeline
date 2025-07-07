CREATE OR REPLACE TABLE `cadastra-teste.APIcripto.rates` (
  id STRING,
  symbol STRING,
  currencySymbol STRING,
  type STRING,
  rateUsd FLOAT64,
  date DATE,
  hour STRING
)
PARTITION BY date;