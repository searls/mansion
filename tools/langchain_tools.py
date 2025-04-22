"""
LangChain tool wrappers for jlistings project.
Each tool is a function with a clear signature and docstring for LLM use.
"""
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from tools.scrape_tool import scrape_listings

class ScrapeInput(BaseModel):
    source: str = Field(description="Listing source, e.g. 'suumo'")
    keyword: str = Field(description="Search keyword, e.g. city or station")
    region: str | None = Field(default=None, description="Optional region code")

def scrape_tool_structured(input: ScrapeInput):
    return scrape_listings(input.source, input.keyword, input.region)

scrape_tool = StructuredTool.from_function(
    scrape_tool_structured,
    name="scrape_tool",
    description="Scrape real estate listings from a given source. Args: source, keyword, region. Returns: list of dicts."
)
