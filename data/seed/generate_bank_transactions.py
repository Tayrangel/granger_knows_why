import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_bank_transactions(n=1000):
    transactions = []
    current_balance = 10000.00
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(n):
        transaction_id = str(uuid.uuid4())
        amount = round(random.uniform(10.0, 5000.0), 2)
        payment_method = random.choice(['credit', 'debit'])
        
        if payment_method == 'debit':
            current_balance -= amount
        else:
            current_balance += amount
            
        event_date = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        # Atraso intencional de 1-3 dias
        processing_date = event_date + timedelta(days=random.randint(1, 3))
        
        # Status: processed (90%), pending (7%), failed (3%)
        status_roll = random.random()
        if status_roll < 0.90:
            status = 'processed'
        elif status_roll < 0.97:
            status = 'pending'
        else:
            status = 'failed'
            
        # Erro intencional 1: ~5% de 'pending' mas balance calculado como if 'processed'
        # (Já está sendo calculado assim no loop acima para simplificar a "armadilha")
        
        transactions.append({
            'transaction_id': transaction_id,
            'amount': amount,
            'payment_method': payment_method,
            'balance_after': round(current_balance, 2),
            'event_date': event_date.isoformat(),
            'processing_date': processing_date.isoformat(),
            'status': status
        })
        
    # Erro intencional 2: ~3% de registros duplicados com ID diferente
    duplicates_count = int(n * 0.03)
    for _ in range(duplicates_count):
        original = random.choice(transactions)
        duplicate = original.copy()
        duplicate['transaction_id'] = str(uuid.uuid4())
        transactions.append(duplicate)
        
    return transactions

if __name__ == "__main__":
    data = generate_bank_transactions(1000)
    print(f"Gerados: {len(data)} registros (incluindo duplicatas)")
    # Exemplo do primeiro registro
    print(data[0])
