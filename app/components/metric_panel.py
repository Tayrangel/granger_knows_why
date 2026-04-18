import streamlit as st
import pandas as pd
import psycopg2
from agent.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

def render_metric_panel():
    st.subheader("📊 Métricas de Hoje")
    
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        df = pd.read_sql("SELECT * FROM fct_revenue ORDER BY reference_date DESC LIMIT 1", conn)
        conn.close()
        
        if not df.empty:
            row = df.iloc[0]
            
            # Custom CSS for larger metrics
            st.markdown("""
                <style>
                [data-testid="stMetricValue"] {
                    font-size: 1.8rem !important;
                    white-space: nowrap;
                }
                </style>
                """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.metric("Receita Bruta", f"R$ {row['gross_revenue']:,.2f}", help="⚠️ Inclui transações não liquidadas.")
                st.metric("TPV", f"R$ {row['tpv']:,.2f}", help="⚠️ Risco de duplicidade entre fontes.")
                st.metric("Saldo Diário", f"R$ {row['daily_balance']:,.2f}")
                
            with c2:
                st.metric("Receita Líquida", f"R$ {row['net_revenue']:,.2f}", delta=f"{row['net_revenue'] - row['gross_revenue']:,.2f}", delta_color="inverse")
                st.metric("Taxa Adquirência", f"{row['acquirer_fee_rate']*100:.2f}%")
        else:
            st.warning("Nenhum dado encontrado no fct_revenue. Execute o pipeline dbt.")
            
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        st.info("💡 Certifique-se de que o PostgreSQL está rodando via Docker.")
