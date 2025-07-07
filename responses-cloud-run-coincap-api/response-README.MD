# Histórico de Execução

Este documento apresenta exemplos de respostas JSON retornadas por um processo de ETL que realiza a inserção de dados em três tabelas principais:

- **Assets** (ativos)
- **Rates** (cotações)
- **History** (histórico de preços)

---

## Exemplo 1: Dados já processados hoje

```json
{
  "assets": {
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Assets."
    },
    "success": true
  },
  "history": {
    "errors": null,
    "results": [],
    "skipped": [
      "Dados para bitcoin já foram processados hoje",
      "Dados para ethereum já foram processados hoje",
      "Dados para tether já foram processados hoje",
      "Dados para xrp já foram processados hoje",
      "Dados para binance-coin já foram processados hoje",
      "Dados para solana já foram processados hoje",
      "Dados para usd-coin já foram processados hoje",
      "Dados para tron já foram processados hoje",
      "Dados para dogecoin já foram processados hoje",
      "Dados para steth já foram processados hoje"
    ],
    "success": true,
    "total_errors": 0,
    "total_processed": 0,
    "total_skipped": 10
  }
}
```

**Resumo**:
- Dados de `Assets` inseridos com sucesso.
- Nenhum dado de `History` processado, pois todos já haviam sido inseridos hoje.

---

## Exemplo 2: Inserção completa com histórico

```json
{
  "assets": {
    "success": true,
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Assets."
    }
  },
  "rates": {
    "success": true,
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Rates."
    }
  },
  "history": {
    "success": true,
    "results": [
      "24 registros históricos inseridos para bitcoin",
      "24 registros históricos inseridos para ethereum"
    ],
    "errors": null,
    "skipped": null,
    "total_processed": 10,
    "total_errors": 0,
    "total_skipped": 0
  }
}
```

**Resumo**:
- Dados de `Assets` e `Rates` inseridos com sucesso.
- Histórico processado e inserido para **bitcoin** e **ethereum**.

---

## Exemplo 3: Erro de execução no histórico

```json
{
  "assets": {
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Assets."
    },
    "success": true
  },
  "history": {
    "errors": [
      "Erro inesperado para bitcoin: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para ethereum: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para tether: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para xrp: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para binance-coin: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para solana: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para usd-coin: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para tron: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para dogecoin: check_execution_date() takes 2 positional arguments but 3 were given",
      "Erro inesperado para steth: check_execution_date() takes 2 positional arguments but 3 were given"
    ],
    "results": [],
    "skipped": null,
    "success": true,
    "total_errors": 10,
    "total_processed": 0,
    "total_skipped": 0
  },
  "rates": {
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Rates."
    },
    "success": true
  }
}
```

**Resumo**:
- Dados de `Assets` e `Rates` inseridos corretamente.
- Erros ocorreram na função `check_execution_date()` ao processar o histórico (erro de argumentos).

---

## Exemplo 4: Dados de histórico já processados

```json
{
  "assets": {
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Assets."
    },
    "success": true
  },
  "history": {
    "errors": null,
    "results": [],
    "skipped": [
      "Dados para bitcoin já foram processados hoje",
      "Dados para ethereum já foram processados hoje",
      "Dados para tether já foram processados hoje",
      "Dados para xrp já foram processados hoje",
      "Dados para binance-coin já foram processados hoje",
      "Dados para solana já foram processados hoje",
      "Dados para usd-coin já foram processados hoje",
      "Dados para tron já foram processados hoje",
      "Dados para dogecoin já foram processados hoje",
      "Dados para steth já foram processados hoje"
    ],
    "success": true,
    "total_errors": 0,
    "total_processed": 0,
    "total_skipped": 10
  },
  "rates": {
    "data": {
      "message": "10 registros inseridos com sucesso na tabela Rates."
    },
    "success": true
  }
}
```

**Resumo**:
- Todos os dados de `Assets` e `Rates` inseridos com sucesso.
- Histórico foi ignorado por já ter sido processado hoje.

---

## Campos importantes

| Campo         | Descrição                                                                 |
|---------------|---------------------------------------------------------------------------|
| `success`     | Indica se a operação foi bem-sucedida.                                    |
| `data.message`| Mensagem de sucesso na inserção de registros.                             |
| `errors`      | Lista de erros encontrados no processamento.                              |
| `results`     | Resultado do processamento (ex: quantos registros foram inseridos).       |
| `skipped`     | Itens ignorados por já terem sido processados.                            |
| `total_*`     | Contadores de erros, processamentos e ignorados.                          |