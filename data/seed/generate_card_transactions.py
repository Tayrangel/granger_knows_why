import uuid
import random
from datetime import datetime, timedelta

def generate_card_transactions(n=1500):
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    
    auth_pool = [] # Para rastrear autorizações que podem ter captura ou cancelamento
    
    for i in range(n):
        transaction_id = str(uuid.uuid4())
        # Tenta reusar um authorization_id se for capture ou cancellation
        event_type = random.choices(['authorization', 'capture', 'cancellation'], weights=[0.6, 0.3, 0.1])[0]
        
        if event_type == 'authorization':
            auth_id = str(uuid.uuid4())
            amount = round(random.uniform(50.0, 3000.0), 2)
            status = random.choices(['approved', 'pending', 'cancelled'], weights=[0.85, 0.1, 0.05])[0]
            event_date = start_date + timedelta(days=random.randint(0, 90))
            
            record = {
                'transaction_id': transaction_id,
                'authorization_id': auth_id,
                'amount': amount,
                'captured_amount': 0,
                'event_type': 'authorization',
                'status': status,
                'event_date': event_date.isoformat()
            }
            if status == 'approved':
                auth_pool.append(record)
        
        elif event_type == 'capture' and auth_pool:
            original = random.choice(auth_pool)
            auth_id = original['authorization_id']
            amount = original['amount']
            
            # Erro intencional: captura parcial
            if random.random() < 0.1:
                captured_amount = round(amount * random.uniform(0.5, 0.95), 2)
            else:
                captured_amount = amount
                
            event_date = datetime.fromisoformat(original['event_date']) + timedelta(hours=random.randint(1, 48))
            
            record = {
                'transaction_id': transaction_id,
                'authorization_id': auth_id,
                'amount': amount,
                'captured_amount': captured_amount,
                'event_type': 'capture',
                'status': 'approved',
                'event_date': event_date.isoformat()
            }
            auth_pool.remove(original) # Capturado
            
        elif event_type == 'cancellation' and auth_pool:
            original = random.choice(auth_pool)
            auth_id = original['authorization_id']
            amount = original['amount']
            
            event_date = datetime.fromisoformat(original['event_date']) + timedelta(hours=random.randint(1, 24))
            
            record = {
                'transaction_id': transaction_id,
                'authorization_id': auth_id,
                'amount': amount,
                'captured_amount': 0,
                'event_type': 'cancellation',
                'status': 'cancelled',
                'event_date': event_date.isoformat()
            }
            auth_pool.remove(original)
        
        else:
            # Fallback se pool vazio ou algo der errado
            auth_id = str(uuid.uuid4())
            amount = round(random.uniform(50.0, 3000.0), 2)
            record = {
                'transaction_id': transaction_id,
                'authorization_id': auth_id,
                'amount': amount,
                'captured_amount': 0,
                'event_type': 'authorization',
                'status': 'pending',
                'event_date': (start_date + timedelta(days=random.randint(0, 90))).isoformat()
            }
            
        transactions.append(record)
        
    return transactions

if __name__ == "__main__":
    data = generate_card_transactions(1500)
    print(f"Gerados: {len(data)} registros")
    # Exemplo
    print(data[0])
