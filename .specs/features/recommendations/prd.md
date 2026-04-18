# 📄 Product Requirements Document (PRD)
Autor: Produto
Status: Rascunho - Aguardando revisão
Última atualização: 18/04/2026
Versão: 0.1

---

## Visão Geral do Produto
Nome do produto: Granger Knows Why
Tipo: Sistema de análise crítica de métricas financeiras com agente inteligente
Categoria: Analytics Engineering + AI Assistant

### Propósito
Ajudar analistas e engenheiros de dados a evitar interpretações incorretas de métricas financeiras, atuando como um agente que questiona conclusões e aponta inconsistências.

### Proposta de valor
Diferente de ferramentas tradicionais que respondem perguntas, o Granger Knows Why desafia respostas.

## Definição do Problema
Métricas financeiras são frequentemente mal interpretadas devido a:
- diferenças entre eventos financeiros (autorização vs liquidação);
- inconsistências entre fontes (banco, cartão, adquirência);
- ausência de contexto sobre qualidade dos dados;
- suposições implícitas em análises SQL;
- falta de validação antes de decisões.

Consequências
- decisões baseadas em dados incorretos;
- distorção de receita e margem;
- perda de confiança em dados;
- retrabalho analítico.


## Usuários-Alvo
Primários:
- Analytics Engineers;
- Data Analysts.

Secundários:
- Data Leads;
- Product Managers com forte uso de dados.

## Escopo do Produto
In Scope (MVP)
- Modelagem de dados financeiros fictícios;
- Camada analítica com métricas;
- Agente que analisa e questiona interpretações;
- Interface para interação com o agente;
- Cenários simulados de erro.

Out of Scope
- Integração com sistemas reais;
- Deploy em produção;
- Escalabilidade enterprise;
- Segurança avançada.

## Domínio de Dados
### Fontes simuladas
1. Extrato bancário
- entradas e saídas financeiras;
- saldo ao longo do tempo.

2. Cartão de crédito
- autorizações;
- capturas;
- cancelamentos.

3. Adquirência
- vendas;
- taxas;
- liquidação.

## Modelo conceitual

Todas as fontes convergem para:
`fct_financial_transactions`

## Complexidades intencionais
- diferença entre valor bruto e líquido;
- atraso de liquidação;
- duplicidade de eventos;
- inconsistência de status;
- cancelamentos parciais.

## Métricas Principais
Receita bruta;
Receita líquida;
TPV (Total Payment Volume);
Taxa de adquirência;
Saldo diário.

## Métricas com armadilhas
- Receita considerando transações não liquidadas;
- TPV com duplicidade;
- Taxa ignorando cancelamentos.

## Funcionalidades do Agente
### Objetivo
Atuar como um analista crítico automatizado.

#### Inputs suportados
- Query SQL;
- Nome de métrica;
- Texto com conclusão analítica.

#### Outputs esperados
- identificação de inconsistências;
- questionamento de premissas;
- explicação de riscos;
- sugestões de validação.

#### Exemplos de comportamento
- Identificar uso incorreto de status financeiro;
- Apontar ausência de granularidade adequada;
- Detectar possíveis vieses de interpretação.

## Cenários de Uso (Use Cases)
1. Validação de métrica
Input: “Receita aumentou 20%”
Output esperado: Questionamento sobre base de cálculo e status das transações.

2. Análise de query
Input: SQL com join incorreto
Output esperado: Identificação de duplicidade ou erro de granularidade.

3. Interpretação de dashboard
Input: Métrica agregada
Output esperado: Explicação de limitações e riscos.

## Arquitetura Técnica
### Componentes
- Banco de dados relacional: PostgreSQL;
- Arquitetura medalhão com motor de transformação de dados: DBT;
- Agente baseado em LLM: LangChain;
- Interface web: Streamlit.

### Fluxo
- Dados brutos carregados;
- Transformação e modelagem;
- Geração de métricas;
- Agente consome contexto;
- Interface exibe análise.

## Experiência do Usuário
Interface
- Input de pergunta ou SQL;
- Visualização de métricas;
- Resposta estruturada do agente.

Estilo de resposta
- didático;
- direto;
- crítico;
- baseado em evidências.

## Critérios de Sucesso
Técnicos
- agente identifica inconsistências reais em pelo menos 3 cenários simulados;
- integração com dados modelados funciona corretamente de ponta a ponta;
- respostas são coerentes com o contexto e citam fontes analíticas quando possível;
- pipeline dbt produz `fct_financial_transactions` e métricas associadas sem erros.

Produto
- clareza na comunicação do problema;
- facilidade de uso da interface;
- capacidade de demonstrar valor em poucos exemplos;
- usuários conseguem validar ou duvidar de uma conclusão com base no feedback do agente.

## Critérios de Aceitação
- Dados simulados gerados e carregados em PostgreSQL com erro intencional controlado.
- Models dbt Bronze/Silver/Gold criados e executáveis.
- Métricas de receita e TPV calculadas com variações de armadilhas plausíveis.
- Agente responde a consultas SQL, nome de métrica e análises textuais.
- Interface apresenta input livre e resposta do agente em formato estruturado.
- Documentação mínima disponível em README e `philosophy.md`.

## Roadmap MVP
1. Setup de ambiente
   - repositório GitHub
   - Docker + PostgreSQL
   - banco `granger_db`
2. Geração e ingestão de dados
   - scripts de geração com Faker
   - tabelas: `bank_transactions`, `card_transactions`, `acquirer_transactions`
   - erros intencionais: status inconsistentes, duplicidade, cancelamentos parciais
3. Modelagem e métricas
   - dbt Bronze/Staging/Silver/Gold
   - tabela final `fct_financial_transactions`
   - métricas principais e armadilhos em `fct_revenue`
4. Agente inteligente
   - prompt base
   - integração com contexto analítico
   - validações de premissas e explicações de risco
5. Interface
   - app Streamlit
   - input de pergunta/SQL
   - exibição de resposta estruturada
6. Narrativa e documentação
   - cenários de erro
   - filosofia do produto
   - README atualizado

## Priorização
- Prioridade alta: dados, modelagem e métricas críticas.
- Prioridade média: agente básico com questionamentos direcionados.
- Prioridade baixa: refinamento da UI e narrativa expandida.

## Dependências e Riscos
Dependências
- PostgreSQL para armazenar dados fictícios;
- dbt para modelagem em camadas;
- LangChain para orquestração do agente;
- Streamlit para interface web.

Riscos
- qualidade dos dados simulados pode não gerar cenários suficientes de erro;
- complexidade do prompt pode reduzir confiança do agente;
- falta de padrões de aceitação pode deixar entregas indefinidas;
- componentes de infraestrutura podem atrasar setup inicial.

## Dados simulados e modelo de domínio
Fontes simuladas principais
- `bank_transactions`: débitos/créditos, saldo, timestamps de processamento.
- `card_transactions`: autorizações, capturas, cancelamentos, status.
- `acquirer_transactions`: vendas, taxas, liquidação e dias de atraso.

Modelo conceitual de tabelas
- `fct_financial_transactions`: transações normalizadas com `transaction_id`, `source`, `amount_gross`, `amount_net`, `status`, `settlement_date`, `event_date`.
- `fct_revenue`: métricas calculadas por período e tipo de evento.

## Trade-offs e Decisões
- uso de dados fictícios para controle de cenários;
- arquitetura simplificada para foco em lógica;
- uso de LLM para interpretação, não para execução.

## Filosofia do Produto
Dados não falham apenas por erro técnico, mas por interpretação incorreta.

O Granger Knows Why existe para garantir que:
- decisões sejam questionadas;
- métricas sejam compreendidas;
- confiança em dados seja construída com rigor.