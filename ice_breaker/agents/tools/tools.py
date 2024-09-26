from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

def get_profile_url_tavily(name:str): 
    load_dotenv()
    """Search for LinkedIn or Twitter profile page"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]
