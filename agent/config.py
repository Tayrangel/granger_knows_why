import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Banco de Dados (PostgreSQL)
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'granger_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'granger')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'granger_pass')

# Configuração do Agente (Groq)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
AGENT_TEMPERATURE = float(os.getenv('AGENT_TEMPERATURE', '0.1'))

# Configuração de Rate Limit
RATE_LIMIT_CALLS = int(os.getenv('RATE_LIMIT_CALLS', '10'))
RATE_LIMIT_PERIOD = int(os.getenv('RATE_LIMIT_PERIOD', '3600')) # 1 hora em segundos

# Configuração de Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
