import os
import json
import time
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from agent.tools import query_metrics_tool, check_data_quality_tool, explain_metric_tool
from agent.context_loader import get_analytics_context
from agent.prompts import GRANGER_SYSTEM_PROMPT
from agent.logger import log_analysis

load_dotenv()

def get_granger_agent(data_context: str) -> AgentExecutor:
    """
    Create and configure the Granger agent.
    
    Args:
        data_context: JSON context with analytics data
        
    Returns:
        Configured AgentExecutor instance
    """
    llm: ChatGroq = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [query_metrics_tool, check_data_quality_tool, explain_metric_tool]

    # Para injetar JSON em prompts do LangChain com segurança, 
    # precisamos escapar as chaves para que o formatador final (f-string)
    # as trate como literais e não como variáveis.
    escaped_context: str = data_context.replace("{", "{{").replace("}", "}}")

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", GRANGER_SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Injetamos o contexto escapado. O LangChain converterá {{ para { no format() final.
    prompt = prompt.partial(data_context=escaped_context)

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def analyze(user_input: str, user_id: str = "user") -> str:
    """
    Analyze user input using the Granger agent.
    
    Args:
        user_input: User's question or assertion
        user_id: User identifier for logging
        
    Returns:
        Agent's response as string
    """
    start_time = time.time()
    try:
        data_context: str = json.dumps(get_analytics_context(), indent=2, ensure_ascii=False)
        
        # Escapa as chaves do JSON para o template engine não as interpretar como variáveis
        data_context_escaped: str = data_context.replace("{", "{{").replace("}", "}}")
        
        system_content: str = GRANGER_SYSTEM_PROMPT.replace("{data_context}", data_context_escaped)
        agent_executor: AgentExecutor = get_granger_agent(system_content)
        response: Dict[str, Any] = agent_executor.invoke({"input": user_input})
        
        result: str = response["output"]
        duration_ms = (time.time() - start_time) * 1000
        log_analysis(user_input, result, duration_ms, 'success')
        
        return result
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_analysis(user_input, str(e), duration_ms, 'error', error=str(e))
        raise

if __name__ == "__main__":
    # Teste rápido
    test_input: str = "Qual o risco do TPV estar alto?"
    print(f"User: {test_input}")
    print(f"Granger: {analyze(test_input)}")
