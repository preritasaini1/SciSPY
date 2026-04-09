import logging
import arxiv
from typing import List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        """Initialize the ResearchAgent with any necessary attributes."""
        self.agent_name = "ResearchAgent"
        self.metadata = {
            'name': self.agent_name,
            'version': '1.0.0',
            'author': 'unknown',
            'description': 'A simple agent for fetching research papers based on a query'
        }
        logger.info(f"{self.agent_name} initialized.")

    def get_papers(self, query: str):
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
    
        papers = []
    
        for result in search.results():
            papers.append({
                "title": result.title,
                "summary": result.summary[:300] + "...",
                "published": str(result.published.date()),
                "url": result.entry_id   # ✅ REAL LINK
            })
    
        return papers
