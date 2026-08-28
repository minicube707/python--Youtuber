from datetime import datetime

from ddgs import DDGS
from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
import requests


@tool("save_text_to_file")
def save_to_txt(
    data: str,
    filename: str = "research_output.txt",
    ) -> str:

    """Save research data to a text file."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


@tool
def search_tool(query: str) -> str:
    """Search the web for information."""

    results = DDGS().text(
        query,
        max_results=5,
    )

    if not results:
        return "No results found."

    return "\n\n".join(
        f"Title: {result.get('title', '')}\n"
        f"URL: {result.get('href', '')}\n"
        f"Snippet: {result.get('body', '')}"
        for result in results
    )


@tool
def wiki_tool(query: str) -> str:
    """Search Wikipedia for a summary of a topic."""

    headers = {"User-Agent": "AI-Agent-Research/1.0 (contact@example.com)"}

    # 1. Find the page title corresponding to the search
    search_resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
        },
        headers=headers,
        timeout=10,
    )

    if search_resp.status_code != 200:
        return f"Wikipedia search failed with status {search_resp.status_code}"

    try:
        search_data = search_resp.json()
    except requests.exceptions.JSONDecodeError:
        return "Wikipedia returned an invalid response (not JSON)."

    results = search_data.get("query", {}).get("search", [])
    if not results:
        return "No Wikipedia results found."

    title = results[0]["title"]

    # 2. Retrieve the summary of the found page
    summary_resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title,
            "format": "json",
        },
        headers=headers,
        timeout=10,
    )

    try:
        summary_data = summary_resp.json()
    except requests.exceptions.JSONDecodeError:
        return "Wikipedia returned an invalid response (not JSON)."

    pages = summary_data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    extract = page.get("extract", "")

    if not extract:
        return f"No content found for page '{title}'."

    return f"Title: {title}\nSummary: {extract[:1000]}"