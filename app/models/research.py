from pydantic import BaseModel, Field
from typing import List

class ResearchRequest(BaseModel):
    """The user's request to start a financial research task."""
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol of the company to research.",
        example="NVDA"
    )
    query: str = Field(
        ...,
        description="The high-level research question or topic.",
        example="Analyze NVIDIA's position in the AI chip market."
    )

class TaskResponse(BaseModel):
    """The response sent back to the user after a task has been initiated."""
    task_id: str = Field(..., description="The unique ID for the research task.", example="abc-123-def-456")
    status: str = Field(..., description="The current status of the task.", example="PENDING")