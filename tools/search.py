from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

def search_headline(headline: str):
    return search_tool.run(headline)
