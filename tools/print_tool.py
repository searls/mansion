from pydantic import BaseModel, Field

class PrintListingsInput(BaseModel):
    listings: list[dict] = Field(description="A list of real estate listing dicts to print as a table.")

# Ensure this function accepts the list directly
def print_listings(listings: list[dict]):
    if not listings:
        return "No listings to display."
    headers = ["title", "price", "address", "station", "layout", "area", "built", "url"]
    table = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for listing in listings: # Iterate directly over the list
        row = [str(listing.get(h, ""))[:40] for h in headers]
        table.append("| " + " | ".join(row) + " |")
    return "\n".join(table)
