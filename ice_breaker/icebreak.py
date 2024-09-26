import os
from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers.string import StrOutputParser
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent 
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from output_parsers import Summary, summary_parser
def ice_break_with(name:str)->Tuple[Summary,str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    twitter_username = twitter_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    tweets = scrape_user_tweets(username=twitter_username)


    summary_template = """
        Given the Linkedin information {information}, and twitter posts {tweets} about a person from I want you to create: 
            - a short summary
            - two interesting facts about them 

        Use both integrations from twitter and linkedin
        \n {format_instructions}
"""
    summary_prompt_template = PromptTemplate(input_variables=["information","tweets"],template=summary_template,
                                             partial_variables={"format_instructions":summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")
    #llm = ChatOllama(model="llama3.1")
    chain = summary_prompt_template | llm | summary_parser
    print(linkedin_data,"linkedin_data")
    print(tweets,"tweets")
    res:Summary = chain.invoke(input={"information":linkedin_data,"tweets":tweets})

    return res,linkedin_data["profile_pic_url"]


if __name__ == "__main__":


    load_dotenv()
    ice_break_with(name="Luis Palomeque del Cerro")