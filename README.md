# 🧙‍♀️ Granger Knows Why
> This project does not answer questions. It challenges answers.

## 🧠 Overview
Granger Knows Why is an AI-powered analytics companion designed to identify flawed interpretations in financial data.

Ao invés de fornecer respostas diretas, o sistema questiona suposições, detecta inconsistências e destaca riscos no raciocínio analítico.

---

## 🚀 Como Iniciar

### 1. Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Uma chave de API do [Groq](https://console.groq.com) (gratuita)

### 2. Configuração do Ambiente
```bash
# Clone o repositório
git clone https://github.com/Tayrangel/granger_knows_why.git
cd granger_knows_why

# Crie seu arquivo .env
cp .env.example .env
# EDITE o .env e adicione sua GROQ_API_KEY
```

### 3. Subir a Infraestrutura (PostgreSQL)
```bash
docker compose up -d db
```

### 4. Instalar Dependências e Gerar Dados
```bash
pip install -r requirements.txt

# Inicializar tabelas e carregar dados simulados
python data/seed/load_all.py
```

### 5. Executar dbt (Transformação de Dados)
```bash
cd dbt
dbt build
cd ..
```

### 6. Iniciar a Interface
```bash
streamlit run app/streamlit_app.py
```

---

## 🧱 Arquitetura e Filosofia

O projeto segue uma modelagem Medalhão (Bronze/Silver/Gold) com contratos de dados rigorosos. Para entender mais sobre os erros propositais e a lógica do agente, veja:
- [📖 Philosophy & Intentional Errors](philosophy.md)

---

## 🧰 Tech Stack
- **PostgreSQL**: Banco de dados relacional (via Docker)
- **dbt-core**: Transformação e qualidade de dados
- **LangChain + Groq (LLaMA 3)**: Orquestração do Agente Crítico
- **Streamlit**: Interface do usuário

---

## 🧪 Casos de Uso (MVP)
1. **Validação de Métricas**: "Receita aumentou 20%" -> Identifica inconsistências no cálculo.
2. **Análise de SQL**: Identifica riscos de duplicidade em queries sem filtros.
3. **Revisão de Decisão**: Questiona premissas implícitas em conclusões de negócio.

---

## 📏 Por que este projeto?
A maioria das ferramentas de analytics foca em dar a resposta mais rápida. O Granger foca em garantir que você não tome uma decisão baseada em uma resposta errada.