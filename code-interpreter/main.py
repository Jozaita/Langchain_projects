from typing import Any
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent,AgentExecutor
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.tools import Tool
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
load_dotenv()


def main():
    print("Start...")

    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    
    tools = [PythonREPLTool()]
    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0,model="gpt-4-turbo"),
        tools=tools
    )

    agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)
    agent_executor.invoke(input={
        "input":"""generate and save in the current directory 2 qrcodes pointing to www.youtube.com, the package qr is already installed."""
    })

    csv_agent = create_csv_agent(llm=ChatOpenAI(temperature=0,model="gpt-4",
                                                path="episode_info.csv",
                                                verbose=True))
    csv_agent.invoke(
        input={"input":"how many columns are there in file episode_info.csv"}
    )

    #Router agent
    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return agent_executor.invoke({"input": original_prompt})
    router_tools = [
        Tool(
            name="Python agent",
            func=python_agent_executor_wrapper,
            description="""Used to transform natural language into python code. It accepts natural language as input and returns the result of a code execution related to the python interpretation of the desired query"""
        ),
        Tool(name="Csv agent",
             func=csv_agent.invoke,
             description="""Used to obtain information about the episode_info csv file. It accepts natural language as input and returns the result of a code execution related to the query. """)
    ]
    
    prompt = base_prompt.partial(instructions=instructions)
    grand_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0,model="gpt-4-turbo"),
        tools=router_tools
    )  

    grand_agent_executor = AgentExecutor(agent=grand_agent,tools=router_tools,verbose=True)

    print(grand_agent_executor.invoke({"input":"Which season has most episodes?"}))


if __name__ == "__main__":
    main()
