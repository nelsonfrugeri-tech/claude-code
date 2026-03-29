# Evaluation SDK — Refinamento de Ideias

## Problema

Criar uma plataforma de evaluation para avaliar aplicações que usam LLM e RAG.
Contexto: assistente bancário com funcionalidades de pagamento por foto, atendimento via FAQ (RAG), etc.
Os times precisam avaliar mudanças (ex: novo node no LangGraph) antes de ir pra produção.

## Decisão: SDK como pytest

O serviço será um **SDK Python** que o dev instala como dependência de dev e usa como pytest.
Classes/funções prontas para cada tipo de eval — o dev importa, compõe e testa.

### Exemplo de uso

```python
from eval_sdk import RAGEval, ToolEval, ClassificationEval, target

@target("http://localhost:8000/invoke")
def my_agent(input): ...

class TestPagamentoNode:

    def test_extrai_boleto(self, my_agent):
        result = my_agent(image="boleto.jpg", msg="paga isso")
        ToolEval(result).assert_called("process_payment", barcode="23793.*")

    def test_faq_pix(self, my_agent):
        result = my_agent(msg="qual o limite do pix?")
        RAGEval(result) \
            .faithfulness(min=0.8) \
            .relevance(min=0.7) \
            .sources_include("faq_pix.md")

    def test_classifica_intencao(self, my_agent):
        result = my_agent(msg="quero cancelar meu cartão")
        ClassificationEval(result) \
            .expected_label("cancelamento") \
            .confidence(min=0.85)
```

```bash
pytest test_pagamento_node.py -v
```

---

## Arquitetura

```
eval-sdk/
├── eval_sdk/
│   ├── __init__.py
│   ├── core/
│   │   ├── target.py        # decorator @target + adapters
│   │   ├── result.py        # EvalResult (contrato universal)
│   │   └── config.py        # settings (judge model, thresholds)
│   ├── evals/
│   │   ├── rag.py           # RAGEval
│   │   ├── tool.py          # ToolEval
│   │   ├── classification.py # ClassificationEval
│   │   ├── conversation.py  # ConversationEval
│   │   ├── summarization.py # SummarizationEval
│   │   └── custom.py        # base pra criar evals custom
│   ├── judges/
│   │   ├── llm.py           # LLM-as-Judge
│   │   ├── heuristic.py     # regex, contains, exact match
│   │   └── composite.py     # combina múltiplos judges
│   ├── datasets/
│   │   └── loader.py        # de YAML, JSON, CSV, HF datasets
│   ├── pytest_plugin/
│   │   └── plugin.py        # fixtures, markers, reporters
│   └── report/
│       └── collector.py     # coleta métricas pra comparação
```

---

## Contrato Universal — EvalResult

```python
@dataclass
class EvalResult:
    response: str
    retrieved_docs: list[Doc] | None = None
    tool_calls: list[ToolCall] | None = None
    classification: Classification | None = None
    metadata: dict = field(default_factory=dict)
    # metadata: latency_ms, tokens_used, model, cost...
```

## @target — Adapters Agnósticos

```python
# LangGraph
@target(adapter="langgraph")
def my_graph(input):
    return graph.invoke({"messages": [HumanMessage(input.msg)]})

# HTTP
@target("http://localhost:8000/invoke")
def my_agent(input): ...

# Função pura (unit test de node isolado)
@target
def my_node(input):
    return llm.invoke(input.msg)
```

---

## 5 Eval Components

### 1. RAGEval

| Método | Descrição |
|---|---|
| `faithfulness(min)` | Resposta fiel aos docs recuperados? |
| `relevance(min)` | Docs recuperados são relevantes? |
| `sources_include(*expected)` | Fontes esperadas foram recuperadas? |
| `no_hallucination()` | Sem info fora dos docs? |
| `answer_correctness(expected, min)` | Semanticamente correta? |

### 2. ToolEval

| Método | Descrição |
|---|---|
| `assert_called(tool, **params)` | Tool chamada com params certos? |
| `assert_not_called(tool)` | Tool NÃO deve ser chamada |
| `call_order(*tools)` | Sequência correta? |
| `call_count(tool, expected)` | Quantidade de invocações |

### 3. ClassificationEval

| Método | Descrição |
|---|---|
| `expected_label(label)` | Output esperado |
| `confidence(min)` | Confiança mínima |
| `not_label(*labels)` | Labels proibidos |

### 4. ConversationEval

| Método | Descrição |
|---|---|
| `tone(expected)` | Tom: formal, friendly, empathetic... |
| `completeness(min)` | Cobre todos os pontos? |
| `toxicity(max)` | Sem conteúdo tóxico |
| `language(expected)` | Idioma correto |
| `follows_guidelines(guidelines)` | Segue diretrizes do negócio |

### 5. SummarizationEval

| Método | Descrição |
|---|---|
| `coverage(key_points, min)` | Cobre pontos-chave? |
| `conciseness(max_ratio)` | Razão resumo/original |
| `no_fabrication()` | Sem info inventada |

---

## Comparação A/B

```bash
pytest test_faq.py --compare baseline=v1.2 candidate=v1.3 --report
```

```
═══════ Comparison Report: v1.2 vs v1.3 ═══════
                  v1.2    v1.3    diff
faithfulness      0.82    0.91    +9%  ✅
relevance         0.88    0.85    -3%  ⚠️
latency_ms        320     290     -9%  ✅
cost              0.003   0.004   +33% ⚠️
═══════════════════════════════════════════════
```

---

## Princípios de Design

| Princípio | Como |
|---|---|
| **Familiar** | Parece pytest — o dev já sabe usar |
| **Composável** | Mixa evals livremente, sem acoplamento |
| **Agnóstico** | `@target` + `EvalResult` abstraem o framework |
| **Não engessa** | Fluent API, tudo opcional, `CustomEval` pra extender |
| **CI-ready** | pytest = já roda no CI do time |

---

## Próximos Passos

1. Implementar `core/` (target + result)
2. Implementar primeiro eval component (RAGEval ou ToolEval)
3. Validar design com caso real do assistente bancário
4. Adicionar LLM-as-Judge
5. Comparação A/B via pytest plugin
