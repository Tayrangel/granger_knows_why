import uuid
import random
from datetime import datetime, timedelta

def generate_acquirer_transactions(card_data, n=1200):
    transactions = []
    
    # Filtra apenas capturas para simular liquidação
    captures = [t for t in card_data if t['event_type'] == 'capture']
    
    for i in range(min(n, len(captures))):
        capture = captures[i]
        transaction_id = str(uuid.uuid4())
        card_transaction_id = capture['transaction_id']
        amount_gross = capture['captured_amount']
        
        # Fee entre 1% e 3%
        fee_rate = random.uniform(0.01, 0.03)
        fee_amount = round(amount_gross * fee_rate, 2)
        
        # Erro intencional: ~8% com amount_net calculado incorretamente (ex: ignorando fee)
        if random.random() < 0.08:
            amount_net = amount_gross # Armadilha!
        else:
            amount_net = round(amount_gross - fee_amount, 2)
            
        capture_date = datetime.fromisoformat(capture['event_date'])
        
        # Status: settled (85%), pending (15%)
        if random.random() < 0.85:
            status = 'settled'
            # Liquidação em D+2 ou D+30
            days_to_settle = random.choice([2, 30])
            settlement_date = (capture_date + timedelta(days=days_to_settle)).date()
        else:
            status = 'pending'
            settlement_date = None
            
        transactions.append({
            'transaction_id': transaction_id,
            'card_transaction_id': card_transaction_id,
            'amount_gross': amount_gross,
            'fee_amount': fee_amount,
            'amount_net': amount_net,
            'settlement_date': settlement_date.isoformat() if settlement_date else None,
            'status': status
        })
        
    return transactions

if __name__ == "__main__":
    from generate_card_transactions import generate_card_transactions
    cards = generate_card_transactions(1500)
    data = generate_acquirer_transactions(cards, 1200)
    print(f"Gerados: {len(data)} registros de adquirência")
    print(data[0])
