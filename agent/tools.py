import os
import time
from typing import Dict, Any, Union
import psycopg2
from langchain.tools import tool
from dotenv import load_dotenv
from agent.logger import log_tool_call

load_dotenv()

def _get_conn() -> psycopg2.extensions.connection:
    """Get database connection."""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )

@tool
def query_metrics_tool() -> Union[Dict[str, Any], str]:
    """Retorna os valores atuais das métricas financeiras consolidadas em fct_revenue."""
    start_time = time.time()
    try:
        conn: psycopg2.extensions.connection = _get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM fct_revenue ORDER BY reference_date DESC LIMIT 1;")
        columns = [desc[0] for desc in cur.description]
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            result = dict(zip(columns, row))
            duration_ms = (time.time() - start_time) * 1000
            log_tool_call('query_metrics_tool', duration_ms, len(str(result)), 'success')
            return result
        
        duration_ms = (time.time() - start_time) * 1000
        log_tool_call('query_metrics_tool', duration_ms, 0, 'success')
        return "Nenhum dado encontrado em fct_revenue."
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_tool_call('query_metrics_tool', duration_ms, 0, 'error', error=str(e))
        return f"Erro ao consultar métricas: {e}"

@tool
def check_data_quality_tool() -> Union[Dict[str, Any], str]:
    """Consulta indicadores de qualidade dos dados (duplicatas, discrepâncias, etc)."""
    start_time = time.time()
    try:
        conn: psycopg2.extensions.connection = _get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                (SELECT count(*) FROM fct_financial_transactions WHERE is_duplicate) as duplicates,
                (SELECT count(*) FROM stg_acquirer_transactions WHERE has_settlement_discrepancy) as settlement_discrepancies,
                (SELECT count(*) FROM fct_financial_transactions WHERE status = 'pending') as pending_transactions
        """)
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        result: Dict[str, Any] = {
            "duplicatas_detectadas": row[0],
            "discrepancias_liquidacao": row[1],
            "transacoes_pendentes": row[2]
        }
        
        duration_ms = (time.time() - start_time) * 1000
        log_tool_call('check_data_quality_tool', duration_ms, len(str(result)), 'success')
        return result
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_tool_call('check_data_quality_tool', duration_ms, 0, 'error', error=str(e))
        return f"Erro ao consultar qualidade: {e}"

@tool
def explain_metric_tool(metric_name: str) -> str:
    """Retorna a definição e as armadilhas associadas a uma métrica específica (ex: 'TPV', 'Receita Bruta')."""
    start_time = time.time()
    definitions: Dict[str, str] = {
        "TPV": "Total Payment Volume. Soma bruta de transações de cartão e adquirência. RISCO: Pode conter duplicidade se as fontes não forem filtradas corretamente (auth vs capture vs acquirer).",
        "Receita Bruta": "Receita total gerada. RISCO: Geralmente inclui transações 'pending' ou não liquidadas, o que pode distorcer a visão de caixa.",
        "Receita Líquida": "Receita após taxas e cancelamentos. No Granger, baseia-se apenas no que foi efetivamente liquidado pelo adquirente.",
        "Taxa de Adquirência": "Custo percentual cobrado pelo adquirente. RISCO: Pode ser mascarado se cancelamentos não forem subtraídos do cálculo da taxa."
    }
    
    result: str = definitions.get(metric_name, f"Definição para '{metric_name}' não encontrada. Tente termos genéricos como TPV ou Receita.")
    duration_ms = (time.time() - start_time) * 1000
    log_tool_call('explain_metric_tool', duration_ms, len(result), 'success')
    return result
