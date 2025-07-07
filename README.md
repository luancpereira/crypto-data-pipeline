# Coleta e Armazenamento de Dados de Criptomoedas

---

## 🚀 Tecnologias Utilizadas

- **Python**: Linguagem principal para chamada da API e manipulação dos dados.
- **Google Cloud Functions + Cloud Run**: Para orquestrar e executar chamadas à API de forma escalável.
- **BigQuery (Google Cloud Platform)**: Armazenamento de dados estruturado e altamente performático.
- **Looker**: Para visualização dos dados tratados.

---

## 📂 Estrutura do Projeto

### 🔄 Orquestração

As chamadas à API da CoinCap são realizadas por uma **Cloud Function**, executando um script Python que consome os dados e os envia para o BigQuery.

### 🗃️ Armazenamento em BigQuery

O projeto foi dividido em dois conjuntos de dados:

#### `APICripto` – Camada Bruta
- Armazena os **dados brutos** provenientes diretamente da API.
- Contém também as **stored procedures** para transformação dos dados.

#### `APICripto_gold` – Camada Tratada (Gold)
- Armazena os dados **tratados, limpos e prontos para análise**.
- Resultado das procedures executadas a partir da camada bruta.

---
