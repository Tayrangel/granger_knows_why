import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from generate_bank_transactions import generate_bank_transactions
from generate_card_transactions import generate_card_transactions
from generate_acquirer_transactions import generate_acquirer_transactions

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )

def load_data():
    print("🚀 Iniciando geração de dados...")
    bank_data = generate_bank_transactions(1000)
    card_data = generate_card_transactions(1500)
    acquirer_data = generate_acquirer_transactions(card_data, 1200)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Bank Transactions
        print("📥 Carregando bank_transactions...")
        cur.execute("TRUNCATE TABLE bank_transactions;")
        execute_values(cur, """
            INSERT INTO bank_transactions (transaction_id, amount, payment_method, balance_after, event_date, processing_date, status)
            VALUES %s
        """, [(t['transaction_id'], t['amount'], t['payment_method'], t['balance_after'], t['event_date'], t['processing_date'], t['status']) for t in bank_data])
        
        # Card Transactions
        print("📥 Carregando card_transactions...")
        cur.execute("TRUNCATE TABLE card_transactions;")
        execute_values(cur, """
            INSERT INTO card_transactions (transaction_id, authorization_id, amount, captured_amount, event_type, status, event_date)
            VALUES %s
        """, [(t['transaction_id'], t['authorization_id'], t['amount'], t['captured_amount'], t['event_type'], t['status'], t['event_date']) for t in card_data])
        
        # Acquirer Transactions
        print("📥 Carregando acquirer_transactions...")
        cur.execute("TRUNCATE TABLE acquirer_transactions;")
        execute_values(cur, """
            INSERT INTO acquirer_transactions (transaction_id, card_transaction_id, amount_gross, fee_amount, amount_net, settlement_date, status)
            VALUES %s
        """, [(t['transaction_id'], t['card_transaction_id'], t['amount_gross'], t['fee_amount'], t['amount_net'], t['settlement_date'], t['status']) for t in acquirer_data])
        
        conn.commit()
        print("✅ Carga finalizada com sucesso!")
        print(f"Resumo: bank={len(bank_data)}, card={len(card_data)}, acquirer={len(acquirer_data)}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro durante a carga: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_data()
