import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage

GRANGER_SYSTEM_PROMPT = """
CONTEXTO DOS DADOS REAIS:
{{data_context}}
"""

data_context = json.dumps({
    "transactions_by_status": {"pending": 10},
    "duplicate_percentage": 5.2
}, indent=2)

system_template = PromptTemplate(
    template=GRANGER_SYSTEM_PROMPT,
    input_variables=["data_context"],
    template_format="mustache"
)
system_prompt_partial = system_template.partial(data_context=data_context)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate(prompt=system_prompt_partial),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

print(f"Variables: {prompt.input_variables}")
