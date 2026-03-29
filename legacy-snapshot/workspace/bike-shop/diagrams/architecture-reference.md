# bike-shop: Multi-Agent Platform Architecture

## Diagrama por Camadas

```
+=========================================================================================+
|                                    USER LAYER                                           |
|                                                                                         |
|                          +---------------------------+                                  |
|                          |      Project Lead         |                                  |
|                          |   (Human Orchestrator)    |                                  |
|                          +-------------+-------------+                                  |
|                                        |                                                |
+=========================================================================================+
                                         | 1. message
                                         v
+=========================================================================================+
|                               COMMUNICATION LAYER                                       |
|                                                                                         |
|                          +---------------------------+                                  |
|                          |         Slack              |                                  |
|                          |   (Socket Mode / WebSocket)|                                 |
|                          +--+----------+----------+--+                                  |
|                             |          |          |                                      |
|                    2. dispatch to bodies (Socket Mode events)                            |
|                             |          |          |                                      |
|                   +---------+--+  +----+-----+  +-+----------+                          |
|                   | Mr. Robot  |  |  Elliot   |  |  Tyrell    |                          |
|                   |  (Body)    |  | Alderson  |  |  Wellick   |                          |
|                   |            |  |  (Body)   |  |  (Body)    |                          |
|                   +-----+------+  +----+------+  +-----+------+                         |
|                         |              |               |                                |
+=========================================================================================+
                          |              |               |
                          +--------------+---------------+
                                         |
                                         | 3. classify intent
                                         v
+=========================================================================================+
|                              INTELLIGENCE LAYER                                         |
|                                                                                         |
|                        +-----------------------------+                                  |
|                        |      Semantic Router        |     +------------------------+   |
|                        |  (runs on Haiku - fast)     |---->|   MODEL SELECTION      |   |
|                        |                             |     |                        |   |
|                        | input -> intent -> agent    |     | +------+ +--------+   |   |
|                        |              + model        |     | | Opus | | Sonnet |   |   |
|                        +------+----------+-----------+     | |(deep)| | (std)  |   |   |
|                               |          |                 | +------+ +--------+   |   |
|                    4. recall()|          |                 |      +-------+        |   |
|                               |          |                 |      | Haiku |        |   |
|                               v          |                 |      |(quick)|        |   |
|                         +-----+----+     |                 |      +-------+        |   |
|                         |   Mem0   |     |                 +------------------------+   |
|                         | recall() |     |                                              |
|                         +----------+     | 5. execute                                   |
|                                          v                                              |
|   +-------------------------------------------+    +-----------------------------+     |
|   |  SPIRITS (~/.claude/agents/)               |    |     Claude Code CLI         |     |
|   |                                            |--->|                             |     |
|   |  +----------+ +-----------+ +--------+    |    |  claude --agent {spirit}    |     |
|   |  | architect | | review-py | | dev-py |    |    |         --model {model}    |     |
|   |  +----------+ +-----------+ +--------+    |    |                             |     |
|   |  +----------+ +-----------+ +---------+   |    +------+------+--------+------+     |
|   |  | debater  | |  tech-pm  | | explorer|   |           |      |        |             |
|   |  +----------+ +-----------+ +---------+   |           |      |        |             |
|   |  +----------+ +-----------+ +----------+  |           |      |        |             |
|   |  | builder  | | sentinel  | |memory-agt|  |           |      |        |             |
|   |  +----------+ +-----+-----+ +----------+  |           |      |        |             |
|   +-------------------------------------------+           |      |        |             |
|                          |                                 |      |        |             |
|                          | monitors                        |      |        |             |
+=========================================================================================+
                           |           |   6. response       |      |        |
                           |           |   to Slack           |      |        |
                           |           +-------> (back up) ---+      |        |
                           |                                         |        |
+=========================================================================================+
|                             INFRASTRUCTURE LAYER                                        |
|                                                                                         |
|  +--------------------+  +------------------+  +----------------+ +------------------+  |
|  |   Mem0             |  |    Langfuse       |  |    GitHub      | |   MCP Tools      |  |
|  |  (Shared Memory)   |  |  (Observability)  |  |                | |                  |  |
|  |                    |  |                   |  | Per-agent Apps | | Notion           |  |
|  | Qdrant (vectors)   |  | Traces           |  | (JWT auth)     | | draw.io          |  |
|  | Ollama             |  | Spans            |  |                | | Excalidraw       |  |
|  |  (nomic-embed-text)|  | Scores           |  | mr-robot-app   | | Langfuse MCP     |  |
|  |                    |  |                   |  | elliot-app     | | memory-keeper    |  |
|  | observe() / recall()|  |                   |  | tyrell-app     | |                  |  |
|  +--------+-----------+  +--------+---------+  +-------+--------+ +---------+--------+  |
|           ^                       ^                     ^                    ^           |
|           |                       |                     |                    |           |
|      7. observe()            8. trace              git ops             tool calls       |
|                                                                                         |
+=========================================================================================+
```

## Fluxo Principal (numerado)

```
1. Project Lead  ----[message]---->  Slack
2. Slack         ----[Socket Mode]-> Body (Mr.Robot | Elliot | Tyrell)
3. Body          ----[classify]----> Semantic Router (Haiku)
                                       |
                                       +--> selects: spirit + model
4. Router        ----[recall()]----> Mem0 (busca contexto relevante)
5. Router        ----[execute]-----> Claude Code CLI
                                       --agent {spirit}
                                       --model {opus|sonnet|haiku}
6. Claude CLI    ----[response]----> Slack (thread reply)
7. Post-exec     ----[observe()]---> Mem0 (salva fatos novos)
8. Post-exec     ----[trace]-------> Langfuse (registra trace completo)
```

## Fluxo do Sentinel (paralelo)

```
Sentinel Agent ---[query traces]---> Langfuse
                                       |
                                       v
                              Analisa anomalias,
                              custos, erros
                                       |
                                       v
                              Reporta no Slack
```

## Identidade dos Bodies vs Spirits

```
+------------------+     +-------------------+
|      BODY        |     |      SPIRIT       |
| (Slack Bot)      |     | (Agent Config)    |
|                  |     |                   |
| - Slack identity |     | - System prompt   |
| - GitHub App     |     | - Allowed tools   |
| - Socket conn    |     | - Behavior rules  |
|                  |     |                   |
| Mr. Robot        |     | architect         |
| Elliot Alderson  |     | dev-py            |
| Tyrell Wellick   |     | review-py         |
+------------------+     | builder           |
        |                 | sentinel          |
        |   ANY body can  | debater           |
        +-- run ANY --->  | tech-pm           |
            spirit        | explorer          |
                          | memory-agent      |
                          +-------------------+
```
