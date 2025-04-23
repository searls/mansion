"""
LangChain tool wrappers for jlistings project.
Each tool is a function with a clear signature and docstring for LLM use.
"""
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from tools.scrape_tool import scrape_listings
from tools.print_tool import print_listings, PrintListingsInput # Import PrintListingsInput

class ScrapeInput(BaseModel):
    source: str = Field(description="Listing source, e.g. 'suumo'")
    keyword: str = Field(description="Search keyword, e.g. city or station")
    region: str | None = Field(default=None, description="Optional region code")

def scrape_tool(input: ScrapeInput):
    return scrape_listings(input.source, input.keyword, input.region)

scrape_tool_structured = StructuredTool.from_function(
    scrape_tool,
    name="scrape_tool",
    description="Scrape real estate listings from a given source. Args: source, keyword, region. Returns: list of dicts."
)

# Define a wrapper that expects the Pydantic model
def print_listings_tool(input: PrintListingsInput):
    return print_listings(input.listings) # Pass the list from the model

# Define the structured tool using the wrapper function
print_listings_structured = StructuredTool.from_function(
    print_listings_tool, # Use the wrapper function
    name="print_listings",
    description="Print a set of real estate listings as a pretty markdown table for the terminal. Input: listings (list of dicts).",
    # args_schema is now inferred from the type hint
)

tools = [
    scrape_tool_structured,
    print_listings_structured,
    # Add enrich_tool and persist_tool here when ready
]
