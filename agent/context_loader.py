import time
from typing import Dict, Any
import psycopg2
from agent.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
from agent.logger import log_context_load

def get_analytics_context() -> Dict[str, Any]:
    """
    Carrega contexto analítico dinâmico do banco para o agente.
    """
    context: Dict[str, Any] = {}
    start_time = time.time()
    
    try:
        conn: psycopg2.extensions.connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cur = conn.cursor()
        
        # 1. Total de transações por status
        cur.execute("SELECT status, count(*) FROM fct_financial_transactions GROUP BY 1;")
        context['transactions_by_status'] = dict(cur.fetchall())
        
        # 2. % de duplicatas
        cur.execute("SELECT count(*) FILTER (WHERE is_duplicate) * 100.0 / count(*) FROM fct_financial_transactions;")
        context['duplicate_percentage'] = round(float(cur.fetchone()[0] or 0), 2)
        
        # 3. % de discrepâncias de liquidação
        cur.execute("SELECT count(*) FILTER (WHERE has_settlement_discrepancy) * 100.0 / count(*) FROM stg_acquirer_transactions;")
        context['settlement_discrepancy_percentage'] = round(float(cur.fetchone()[0] or 0), 2)
        
        # 4. Período dos dados
        cur.execute("SELECT MIN(COALESCE(event_date, settlement_date)), MAX(COALESCE(event_date, settlement_date)) FROM fct_financial_transactions;")
        dates = cur.fetchone()
        context['date_range'] = {'min': str(dates[0]), 'max': str(dates[1])}
        
        cur.close()
        conn.close()
        
        duration_ms = (time.time() - start_time) * 1000
        log_context_load(duration_ms, 'success')
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_context_load(duration_ms, 'error', error=str(e))
        
        # Retorna contexto básico estático para não bloquear o agente totalmente
        context = {
            'warning': 'Dados reais indisponíveis. Usando contexto genérico.',
            'duplicate_percentage': 'Desconhecida (risco alto)',
            'settlement_discrepancy_percentage': 'Desconhecida (risco alto)'
        }
        
    return context

if __name__ == "__main__":
    import json
    print(json.dumps(get_analytics_context(), indent=2))
