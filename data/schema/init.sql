-- Tabela de Transações Bancárias
CREATE TABLE IF NOT EXISTS bank_transactions (
    transaction_id UUID PRIMARY KEY,
    amount NUMERIC(15, 2) NOT NULL,
    payment_method TEXT NOT NULL, -- 'credit' ou 'debit'
    balance_after NUMERIC(15, 2) NOT NULL,
    event_date TIMESTAMP NOT NULL,
    processing_date TIMESTAMP NOT NULL,
    status TEXT NOT NULL -- 'processed', 'pending', 'failed'
);

-- Tabela de Transações de Cartão
CREATE TABLE IF NOT EXISTS card_transactions (
    transaction_id UUID PRIMARY KEY,
    authorization_id UUID NOT NULL,
    amount NUMERIC(15, 2) NOT NULL,
    captured_amount NUMERIC(15, 2),
    event_type TEXT NOT NULL, -- 'authorization', 'capture', 'cancellation'
    status TEXT NOT NULL, -- 'approved', 'cancelled', 'pending'
    event_date TIMESTAMP NOT NULL
);

-- Tabela de Transações de Adquirência
CREATE TABLE IF NOT EXISTS acquirer_transactions (
    transaction_id UUID PRIMARY KEY,
    card_transaction_id UUID NOT NULL,
    amount_gross NUMERIC(15, 2) NOT NULL,
    fee_amount NUMERIC(15, 2) NOT NULL,
    amount_net NUMERIC(15, 2) NOT NULL,
    settlement_date DATE,
    status TEXT NOT NULL -- 'pending', 'settled', 'reversed'
);

-- Índices para Performance
CREATE INDEX IF NOT EXISTS idx_bank_transactions_event_date ON bank_transactions(event_date);
CREATE INDEX IF NOT EXISTS idx_bank_transactions_status ON bank_transactions(status);

CREATE INDEX IF NOT EXISTS idx_card_transactions_event_date ON card_transactions(event_date);
CREATE INDEX IF NOT EXISTS idx_card_transactions_status ON card_transactions(status);

CREATE INDEX IF NOT EXISTS idx_acquirer_transactions_settlement_date ON acquirer_transactions(settlement_date);
CREATE INDEX IF NOT EXISTS idx_acquirer_transactions_status ON acquirer_transactions(status);
