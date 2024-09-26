from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent,AgentExecutor
from langchain import hub

from agents.tools.tools import get_profile_url_tavily 

def lookup(name:str)->str:
    #llm = ChatOllama(model="llama3.1",temperature=0)
    llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")

    template = """
    given the full name {name} I want you to get a link for their Twitter profile page. Your answer should contain just the  twitter username """

    prompt_template = PromptTemplate(template=template,input_variables=["name"])

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="useful when you need to crawl a Twitter profile"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True)

    result = agent_executor.invoke(input={"input":prompt_template.format_prompt(name=name)})
    linked_profile_url = result["output"]
    return linked_profile_url

if __name__ == "__main__":
    load_dotenv()
    linkedin_url = lookup(name="Juan Ozaita")