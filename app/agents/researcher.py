import asyncio
import json
from mistralai.client import MistralClient

from ..core.config import settings
from ..tools import news, financials

client = None
if settings.MISTRAL_API_KEY:
    client = MistralClient(api_key=settings.MISTRAL_API_KEY)

AVAILABLE_TOOLS = {
    "fetch_news": news.fetch_news,
    "fetch_company_overview": financials.fetch_company_overview,
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "fetch_news",
            "description": "Fetches recent news articles for a given company ticker or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The company ticker or name to search news for.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_company_overview",
            "description": "Fetches company overview and key financial metrics from Alpha Vantage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol of the company.",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
]

async def run_researcher(ticker: str, query: str) -> dict:
    """
    Runs the Researcher agent to gather data using tool-calling with Mistral.
    """
    if not client:
        print("Error: Mistral client not initialized. Check MISTRAL_API_KEY.")
        return {}

    print("-> Researcher Agent: Starting...")
    
    system_prompt = "You are an expert financial researcher. Your goal is to gather data to answer the user's query by selecting the appropriate tools."
    user_message = f"Ticker: {ticker}\nQuery: {query}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    response = client.chat(
        model="mistral-small-latest", 
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)
    
    if not assistant_message.tool_calls:
        print("-> Researcher Agent: The model decided not to call any tools.")
        return {"summary": "No data gathered as no tools were selected."}
    
    tasks = []
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name in AVAILABLE_TOOLS:
            print(f"-> Researcher Agent: Calling tool '{function_name}' with args {function_args}")
            tasks.append(
                asyncio.create_task(AVAILABLE_TOOLS[function_name](**function_args))
            )

    tool_results = await asyncio.gather(*tasks)

    final_data = {}
    for i, tool_call in enumerate(assistant_message.tool_calls):
        final_data[tool_call.function.name] = tool_results[i]

    print("-> Researcher Agent: Finished gathering data.")
    return final_data