from fastapi import FastAPI

app = FastAPI(
    title="Delphi",
    description="A multi-agent system for automated financial research.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "Delphi is online."}