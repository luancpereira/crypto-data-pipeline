
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
  <summary><strong>🔧 bigquery_functions.py</strong></summary>

Funções auxiliares para interação com o BigQuery:

- `insert_into_bigquery(rows, table, chunk_size)`:  
  Insere dados em qualquer tabela do BigQuery de forma escalável via chunking.

- `check_execution_date(crypto)`:  
  Verifica a última execução de uma determinada criptomoeda para evitar reprocessamento.

- `insert_log_entry(error)`:  
  Insere registros de erro na tabela de log.

</details>

<details>
  <summary><strong>etl.py</strong></summary>

Responsável pela transformação dos dados para os formatos compatíveis com o BigQuery:

- `transform_assets_data(data)`  
- `transform_rates_data(data)`  
- `transform_assets_history_data(data)`  

Essas funções garantem que os dados estejam no formato correto e com os tipos apropriados para evitar falhas de carregamento.

</details>

<details>
  <summary><strong>externals_apis.py</strong></summary>

Responsável pelas chamadas externas à API CoinCap:

- `get_assets_data()`  
- `get_rates_data()`  
- `get_assets_history_data()`  

Cada função realiza tratamento de parâmetros, erros e retorno das respostas de forma padronizada.

</details>

<details>
  <summary><strong>service.py</strong></summary>

Coordena o fluxo completo de dados:

- `process_assets_data()`  
- `process_rates_data()`  
- `process_assets_history_data()`:  
  Executa uma verificação no BigQuery para garantir que o histórico da cripto não foi processado no dia antes de continuar. Processa dados individualmente por cripto, em uma estrutura de repetição.

</details>

<details>
  <summary><strong>utils.py</strong></summary>

Funções utilitárias reutilizadas em diversas partes do projeto. Auxiliam na padronização e organização da lógica.

</details>

<details>
  <summary><strong>main.py</strong></summary>

Ponto de entrada principal da aplicação no Cloud Run:

- Realiza a chamada das funções de `service.py`
- Trata erros e logs
- Realiza leitura do token e do corpo da requisição enviada ao endpoint

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

A aplicação foi construída para ser executada via **Google Cloud Run**, onde o endpoint exposto é responsável por:

1. Realizar chamadas às APIs de criptomoedas;
2. Transformar os dados para o formato do BigQuery;
3. Verificar execuções anteriores (quando necessário);
4. Inserir os dados em lote no BigQuery de forma escalável (`chunking`);
5. Registrar falhas ou erros no log.

---