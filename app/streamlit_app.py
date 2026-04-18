import streamlit as st
import json
from typing import Optional
from components.metric_panel import render_metric_panel
from components.response_card import render_response_card
from agent.agent import analyze
from agent.rate_limiter import api_rate_limiter, RateLimitExceeded

st.set_page_config(page_title="Granger Knows Why", page_icon="🕵️", layout="wide")

st.title("🕵️ Granger Knows Why")
st.markdown("*O agente financeiro que não responde, ele questiona.*")

# Layout principal
col1, col2 = st.columns([3, 1])

with col1:
    render_metric_panel()
    
    st.markdown("---")
    st.subheader("💡 Exemplos de Cenários")
    if st.button("Cenário 1: Receita inflada"):
        st.session_state.user_input = "A receita bruta aumentou 20% este mês. Podemos investir mais?"
    if st.button("Cenário 2: Erro de SQL"):
        st.session_state.user_input = "SELECT SUM(amount) FROM card_transactions"
    if st.button("Cenário 3: Dúvida sobre TPV"):
        st.session_state.user_input = "O TPV reportado pelo adquirente não bate com o banco."

with col2:
    st.subheader("🔍 Nova Análise")
    user_input = st.text_area(
        "Insira uma query SQL, nome de métrica ou conclusão analítica:",
        value=st.session_state.get("user_input", ""),
        height=150
    )
    
    # Display rate limit info
    remaining_calls = api_rate_limiter.get_remaining('user')
    st.caption(f"📊 Análises restantes: {remaining_calls}/10 por hora")
    
    if st.button("Analisar com Granger"):
        if user_input:
            # Check rate limit
            if not api_rate_limiter.is_allowed('user'):
                st.error("❌ Limite de requisições atingido (10 por hora)")
                st.info("💡 Por favor, tente novamente depois de uma hora")
            else:
                with st.spinner("Granger está analisando as armadilhas..."):
                    try:
                        response = analyze(user_input, user_id='user')
                        api_rate_limiter.request_times['user'].append(0)  # Record the request
                        render_response_card(response)
                    except RateLimitExceeded as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"Erro ao processar análise: {e}")
                        st.info("💡 Verifique se sua GROQ_API_KEY está correta no .env")
        else:
            st.warning("Por favor, insira algum texto para análise.")

st.sidebar.markdown("""
### Sobre o Granger
O Granger utiliza **LLaMA 3 (via Groq)** para realizar análises críticas de dados simulados no PostgreSQL.
Sua missão é evitar erros de interpretação em KPIs financeiros.
""")
