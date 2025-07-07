CREATE OR REPLACE TABLE `cadastra-teste.APIcripto.assets` (
  id STRING,
  rank INT64,
  symbol STRING,
  name STRING,
  supply FLOAT64,
  maxSupply FLOAT64,
  marketCapUsd FLOAT64,
  volumeUsd24Hr FLOAT64,
  priceUsd FLOAT64,
  changePercent24Hr FLOAT64,
  vwap24Hr FLOAT64,
  explorer STRING,
  date DATE,
  hour STRING
)
PARTITION BY date;