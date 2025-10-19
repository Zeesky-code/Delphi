from fastapi import FastAPI, BackgroundTasks
from .models.research import ResearchRequest, TaskResponse

app = FastAPI(
    title="Delphi",
    description="A multi-agent system for automated financial research.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "Delphi is online."}

@app.post("/research/", response_model=TaskResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Accepts a research request and starts the Delphi agent workflow.
    """
    task_id = str(uuid.uuid4())
    
    background_tasks.add_task(run_delphi_workflow, request.ticker, request.query)
    return TaskResponse(task_id=task_id, status="PENDING")
