import streamlit as st
import re

def render_response_card(response_text):
    st.markdown("---")
    st.subheader("🕵️ Análise do Granger")
    
    # Tenta extrair as 3 seções usando regex
    sections = {
        "Inconsistências": "⚠️ Inconsistências",
        "Riscos": "🔴 Riscos",
        "Validações Sugeridas": "✅ Validações Sugeridas"
    }
    
    parts = re.split(r'\n\d\.\s\*\*', response_text)
    
    # Se não conseguirmos splitar corretamente, exibe o texto bruto com estilo
    if len(parts) < 2:
        st.info(response_text)
        return

    # Mapeamento simples (assumindo a ordem do prompt)
    for part in parts:
        if "Inconsistências" in part:
            st.warning(part.replace("**Inconsistências**:", "").strip())
        elif "Riscos" in part:
            st.error(part.replace("**Riscos**:", "").strip())
        elif "Validações Sugeridas" in part:
            st.success(part.replace("**Validações Sugeridas**:", "").strip())
        elif part.strip():
            st.markdown(part.strip())
