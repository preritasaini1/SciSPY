from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryModel(BaseModel):
    query: str

@app.post("/search_papers/")
async def search_papers(query: QueryModel):
    # Simulating response for the query
    # Replace with real logic to fetch papers
    papers = [
        {"title": f"Paper on {query.query}", "abstract": f"Abstract of {query.query} paper."}
    ]
    return {"papers": papers}
