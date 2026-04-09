from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from heurist_agent import ResearchAgent  # Import Heurist agent

app = FastAPI()

# Enable CORS to allow requests from frontend (localhost:8001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Only allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize Heurist agent
agent = ResearchAgent()

class QueryModel(BaseModel):
    query: str

@app.post("/search_papers/")
async def search_papers(query: QueryModel):
    papers = await agent.fetch_papers(query.query) # Fetch papers using the agent
    return {"papers": papers}
