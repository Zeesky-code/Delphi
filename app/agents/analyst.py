import json
from mistralai.client import MistralClient

from ..core.config import settings

client = None
if settings.MISTRAL_API_KEY:
    client = MistralClient(api_key=settings.MISTRAL_API_KEY)

async def run_analyst(research_data: dict, query: str) -> str:
    """
    Synthesize research data into a report.
    """
    if not client:
        print("Error: Mistral client not initialized.")
        return "Error: Analyst agent not configured."

    print("-> Analyst Agent: Starting analysis...")

    data_string = json.dumps(research_data, indent=2)

    system_prompt = """
    You are a senior financial analyst at a top-tier investment firm. Your task is to write a concise, insightful, and well-structured investment summary based on the provided raw data.

    Follow these instructions:
    1.  **Start with a clear summary** of the company's current situation based on the user's query.
    2.  **Synthesize key points** from both the quantitative (financial overview) and qualitative (news) data. Do not just list the data; explain what it means.
    3.  **Address the user's original query** directly.
    4.  **Use Markdown formatting** for clarity (e.g., headings, bold text, bullet points).
    5.  **Maintain a professional and objective tone.**
    """

    user_prompt = f"""
    Please generate a financial summary for the following query: "{query}"

    Here is the raw data my research team has gathered:
    ---
    {data_string}
    ---
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat(
        model="mistral-small-latest",
        messages=messages,
    )

    summary = response.choices[0].message.content
    print("-> Analyst Agent: Finished analysis.")
    return summary