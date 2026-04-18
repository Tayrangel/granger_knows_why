import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

GRANGER_SYSTEM_PROMPT = """
CONTEXTO DOS DADOS REAIS:
{data_context}
"""

data_context = json.dumps({
    "transactions_by_status": {"pending": 10},
    "duplicate_percentage": 5.2
}, indent=2)

system_content = GRANGER_SYSTEM_PROMPT.replace("{data_context}", data_context)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_content),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

print(f"Variables: {prompt.input_variables}")
print(f"Messages count: {len(prompt.messages)}")
print(f"Message 0 type: {type(prompt.messages[0])}")
