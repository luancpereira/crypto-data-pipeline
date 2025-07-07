
# Coleta e Armazenamento de Dados de Criptomoedas

---

## Tecnologias Utilizadas

- **Python**: Utilizado para chamadas à API, transformação e orquestração dos dados.
- **Google Cloud Functions + Cloud Run**: Execução e orquestração do pipeline. O **Cloud Run** executa a chamada da API e realiza o salvamento dos dados no BigQuery de forma performática.
- **BigQuery (Google Cloud Platform)**: Armazenamento estruturado e escalável para os dados coletados.
- **Apache Airflow**: Orquestração e agendamento do pipeline de dados.
- **Looker**: Visualização dos dados tratados.

---

## Estrutura do Projeto no Cloud Run

O diretório `cloud-run-coincap-api` contém toda a lógica responsável pela coleta, transformação e carga de dados.

<details>
  <summary><strong>bigquery_functions.py</strong></summary>

Funções auxiliares para interação com o BigQuery:

- `insert_into_bigquery(rows, table, chunk_size)`:  
  Insere dados em qualquer tabela do BigQuery de forma escalável via chunking.

- `check_execution_date(crypto_id, current_date)`:  
  Verifica a última execução de uma determinada criptomoeda para evitar reprocessamento.

- `insert_log_entry(crypto_id, status, json_error, timestamp_hour)`:  
  Insere registros de erro na tabela de log.
</details>

<details>
  <summary><strong>etl.py</strong></summary>

Responsável pela transformação dos dados para os formatos compatíveis com o BigQuery:

- `transform_assets_data(json_data)`  
- `transform_rates_data(json_data)`  
- `transform_assets_history_data(json_data, crypto_id, execution_date)`  
</details>

<details>
  <summary><strong>externals_apis.py</strong></summary>

Responsável pelas chamadas externas à API CoinCap:

- `get_assets_data(token, ids=None)`  
- `get_rates_data(token, ids=None)`  
- `get_assets_history_data(token, crypto_id, start_timestamp, end_timestamp)`  
</details>

<details>
  <summary><strong>service.py</strong></summary>

Coordena o fluxo completo de dados:

- `process_assets_data(token, cryptos)`  
- `process_rates_data(token, cryptos)`  
- `process_assets_history_data(token, cryptos)`  
</details>

<details>
  <summary><strong>utils.py</strong></summary>

Funções utilitárias reutilizadas em diversas partes do projeto.
</details>

<details>
  <summary><strong>main.py</strong></summary>

Ponto de entrada principal da aplicação no Cloud Run.
</details>

<details>
  <summary><strong>constants.py</strong></summary>

Armazena variáveis globais, configurações e nomes de tabelas:

```python
import os

class Config:
    API_URL = os.environ.get("API_URL")
    BIGQUERY_DATASET = "cadastra-teste.APIcripto"
    BATCH_SIZE = 500

class TableNames:
    ASSETS = f"{Config.BIGQUERY_DATASET}.assets"
    RATES = f"{Config.BIGQUERY_DATASET}.rates"
    ASSETS_HISTORY = f"{Config.BIGQUERY_DATASET}.assets_history"
    LOG_EXECUTION = f"{Config.BIGQUERY_DATASET}.log_execution"
```
</details>

---

## Funcionamento Geral no Cloud Run

A aplicação é executada via **Google Cloud Run**, com um endpoint exposto que:

1. Realiza chamadas às APIs de criptomoedas;
2. Transforma os dados para o formato do BigQuery;
3. Verifica execuções anteriores (quando necessário);
4. Insere os dados em lote no BigQuery de forma escalável (chunking);
5. Registra falhas ou erros no log.

---

## Estrutura de Armazenamento no BigQuery

A arquitetura de dados segue o conceito de **camadas**, com dois conjuntos de dados principais:

### 🔹 `APIcripto` (Camada Bruta)

Conjunto de dados que armazena informações brutas obtidas diretamente da API e também procedures intermediárias de transformação.

#### Tabelas brutas

- `cadastra-teste.APIcripto.assets`  
- `cadastra-teste.APIcripto.rates`  
- `cadastra-teste.APIcripto.assets_history`  

> As queries de definição estão na pasta: `bigquery/tables`

#### Procedures

> Localizadas em: `bigquery/procedures`

- `best_performers_last_24h`:  
  Gera ranking das criptomoedas com **melhor e pior performance nas últimas 24 horas**, categorizadas em:
  - `up`: crescimento
  - `down`: queda

- `crypto_analysis_by_hour`:  
  Executa análise horária das criptos e evita reprocessamento de dados já existentes.

- `latest_rates`:  
  Atualiza as **últimas cotações** disponíveis das criptomoedas.

---

### `APIcripto_gold` (Camada Tratada)

Conjunto com os **dados prontos para análise**, resultado das procedures da camada bruta.

#### Tabelas tratadas

- `cadastra-teste.APIcripto_gold.latest_rates`  
- `cadastra-teste.APIcripto_gold.crypto_analysis_by_hour`  
- `cadastra-teste.APIcripto_gold.best_performers_last_24h`  

Essas tabelas servem como base para visualizações no **Looker** e demais análises de negócio.

---