
# Coleta e Armazenamento de Dados de Criptomoedas

**Link do Looker**: https://lookerstudio.google.com/s/vgb9fT77bPs

## Dashboard de Criptomoedas

Este projeto tem como resultado final um dashboard interativo desenvolvido no Looker Studio, com foco no monitoramento de criptomoedas. O painel exibe:

- Cotação atual em USD e BRL
- Variação percentual nas últimas 24 horas
- Criptomoeda com maior valorização no dia
- Volume total negociado nas últimas 24h
- Market Cap agregado
- Distribuição de volume por criptomoeda em gráfico de pizza
- Análise horária da volatilidade dos preços

Com isso, é possível obter uma visão clara e rápida do mercado cripto, facilitando decisões estratégicas e o acompanhamento de tendências.

---

# Configuração e Execução do Projeto

## Pré-requisitos

### 1. Configurações no Google Cloud Platform

Para executar o projeto em nuvem, é necessário ativar os seguintes serviços do **Google Cloud Platform**:

- **Cloud Run** - Para hospedagem do serviço de coleta
- **BigQuery** - Para armazenamento e processamento dos dados

### 2. Service Account

Gere o arquivo JSON de **Service Account** no GCP com as permissões necessárias para:
- Acessar o BigQuery
- Executar serviços no Cloud Run

## Configuração do Apache Airflow

### 1. Instalação do Docker

Certifique-se de ter o **Docker** e **Docker Compose** instalados em sua máquina.

### 2. Estrutura de Diretórios

Crie a seguinte estrutura de diretórios no seu ambiente Airflow:

```
airflow/
├── dags/
├── credenciais/
│   └── gcp-sa.json
├── docker-compose.yaml
└── .env
```

### 3. Configuração do Arquivo .env

Crie um arquivo `.env` na raiz do diretório do Airflow com as seguintes variáveis:

```bash
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=/home/luan/airflow  # Substitua pelo seu diretório local do Airflow
```

> **Nota**: Ajuste o `AIRFLOW_PROJ_DIR` para o caminho correto do seu diretório do Airflow.

### 4. Configuração do Docker Compose

No arquivo `docker-compose.yaml`, adicione o seguinte mapeamento de volume na seção `volumes`:

```yaml
volumes:
  - ${AIRFLOW_PROJ_DIR:-.}/credenciais/gcp-sa.json:/opt/airflow/gcp-sa.json
```

Esta configuração mapeia suas credenciais do GCP para dentro do container do Airflow.

### 5. Adicionando a DAG

Copie o arquivo `execute_all_services.py` para a pasta `dags/` criada anteriormente.

## Executando o Projeto

### 1. Inicialização do Airflow

Execute o comando para inicializar o Airflow:

```bash
sudo docker compose up
```

Aguarde o carregamento completo do sistema.

### 2. Acesso à Interface Web

Após a inicialização, acesse a interface web do Airflow em:

```
http://localhost:8080/
```

### 3. Credenciais de Acesso

Use as seguintes credenciais padrão para fazer login:

- **Usuário**: `airflow`
- **Senha**: `airflow`

### 4. Verificação da DAG

Na interface web, você poderá visualizar e monitorar a DAG `execute_all_services` e suas execuções horárias.

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

# Orquestração com Apache Airflow

O processo de orquestração do pipeline de dados é realizado por meio do **Apache Airflow**, utilizando uma DAG configurada para rodar de **hora em hora**.

## Estrutura da DAG

A DAG principal está localizada no diretório:
```
airflow-execute-services/execute_all_services.py
```

### Fluxo de Execução

A DAG realiza duas etapas principais executadas sequencialmente:

## 1. Execução do Serviço no Cloud Run

A função `execute_services()` é responsável por acionar o serviço exposto no **Cloud Run** através do endpoint:

```
https://coincap-api-753104042367.us-central1.run.app
```

### Parâmetros Enviados

Na chamada do serviço, são enviadas as seguintes criptomoedas de interesse:

```python
cryptos = [
    "bitcoin",
    "ethereum", 
    "tether",
    "xrp",
    "binance-coin",
    "solana",
    "usd-coin",
    "tron",
    "dogecoin",
    "steth"
]
```

### Funcionalidades do Serviço

Este serviço executa toda a lógica de:
- **Coleta** de dados das criptomoedas
- **Transformação** dos dados coletados
- **Carga** dos dados no BigQuery
- **Registro de erros** (quando necessário)

## 2. Execução das Procedures no BigQuery

Somente após a execução **bem-sucedida** do serviço no Cloud Run, a DAG avança para a próxima etapa.

### Procedures Executadas

A execução das procedures é realizada através da função `execute_bigquery_procedure(procedure_query)` e inclui:

- `best_performers_last_24h`
- `crypto_analysis_by_hour`
- `latest_rates`

### Processamento Concorrente

Como essas procedures são **independentes** entre si, elas são executadas de forma **concorrente**, otimizando o tempo de processamento da DAG.

## Frequência de Execução

- **Intervalo**: A cada hora
- **Tipo**: Agendamento automático via Apache Airflow

## Dependências

1. **Apache Airflow** - Orquestrador principal
2. **Google Cloud Run** - Hospedagem do serviço de coleta
3. **Google BigQuery** - Armazenamento e processamento de dados

---