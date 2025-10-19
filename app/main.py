from fastapi import FastAPI, BackgroundTasks
from .models.research import ResearchRequest, TaskResponse
from .tools.news import fetch_news
import uuid

app = FastAPI(
    title="Delphi",
    description="A multi-agent system for automated financial research.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "Delphi is online."}

async def run_delphi_workflow(ticker: str, query: str):
    print(f"--- Starting Delphi Workflow for {ticker} ---")
    print(f"Query: {query}")
    
    articles = await fetch_news(ticker)
    print(f"Found {len(articles)} articles for {ticker}:")
    for article in articles:
        print(f"- {article['title']}")
    
    print("--- Delphi Workflow Finished ---")

@app.post("/research/", response_model=TaskResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Accepts a research request and starts the Delphi agent workflow.
    """
    task_id = str(uuid.uuid4())
    
    background_tasks.add_task(run_delphi_workflow, request.ticker, request.query)
    
    return TaskResponse(task_id=task_id, status="PENDING")
