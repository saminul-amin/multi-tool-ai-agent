import os
import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from tools.db_tools import InstitutionsDBTool, HospitalsDBTool, RestaurantsDBTool
from tools.search_tool import get_web_search_tool

load_dotenv()

REACT_PROMPT = PromptTemplate.from_template(
    """You are a helpful AI assistant specialized in answering questions about Bangladesh.
You have access to three databases (institutions, hospitals, restaurants) and a web search tool.

IMPORTANT RULES:
1. For data/statistics questions, use the appropriate database tool by writing a valid SQLite SQL query.
2. For general knowledge questions, use the WebSearchTool.
3. Always think step-by-step before choosing a tool.
4. Division/district names in the institutions database are UPPERCASE (e.g., 'DHAKA', 'CHATTOGRAM').
5. Division/district names in the hospitals database are Title Case (e.g., 'Dhaka', 'Chattogram').
6. When writing SQL, always include a LIMIT clause (e.g., LIMIT 20) to avoid huge results.
7. Use LIKE with wildcards for partial text matching (e.g., WHERE name LIKE '%biryani%').

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: I should think about which tool to use and what query to write
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
) # idk what it says... AI given this message!

def create_llm():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "You need to beg for tokens buddy! ;)"
        )

    endpoint = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        task="conversational",
        huggingfacehub_api_token=hf_token,
        temperature=0.1,
        max_new_tokens=1024,
    )
    llm = ChatHuggingFace(llm=endpoint)
    return llm

def create_agent_executor():
    llm = create_llm()
    tools = [
        InstitutionsDBTool,
        HospitalsDBTool,
        RestaurantsDBTool,
        get_web_search_tool(),
    ]
    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        return_intermediate_steps=True,
    )
    return agent_executor


def run_query(agent_executor, query: str) -> str:
    result = agent_executor.invoke({"input": query})
    return result["output"]
