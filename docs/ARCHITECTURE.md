# Arquitetura

O projeto utiliza uma arquitetura modular.

```
Collector
      ↓
Model
      ↓
Analyzer
      ↓
Presenter
      ↓
CLI
```

## Collector

Responsável por coletar informações.

Nunca apresenta dados.

Nunca imprime informações.

---

## Model

Representa entidades do domínio.

Não realiza consultas.

Não imprime informações.

---

## Analyzer

Realiza comparações, validações e correlações.

---

## Presenter

Transforma modelos em relatórios legíveis.

---

## CLI

Interface utilizada pelo operador.
