from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from mesh.research_agent import ResearchAgent

app = FastAPI()

class QueryModel(BaseModel):
    query: str

class PaperAnalysisModel(BaseModel):
    url: str

class QuestionModel(BaseModel):
    url: str
    query: str

@app.post("/search_papers/")
async def search_papers(query: QueryModel):
    """Fetch research papers using Mesh Agent."""
    agent = ResearchAgent()
    papers = await agent.fetch_papers(query.query)
    
    if not papers:
        return {"papers": []}

    return {"papers": papers}

@app.post("/fetch_paper_content/")
async def fetch_paper_content(query: PaperAnalysisModel):
    """Extract paper content using Mesh Agent."""
    agent = ResearchAgent()
    try:
        content = await agent.extract_text(query.url)
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer_query/")
async def answer_query(query: QuestionModel):
    """Answer user questions based on extracted paper content."""
    agent = ResearchAgent()

    # Extract paper content first
    pdf_text = await agent.extract_pdf_content(query.url)
    if not pdf_text:
        raise HTTPException(status_code=400, detail="Failed to extract PDF content")

    # Answer the query
    answer = await agent.answer_query(pdf_text, query.query)
    return {"answer": answer}
