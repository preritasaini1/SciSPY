import logging
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

    def get_papers(self, query: str) -> List[str]:
        """Fetch research papers based on the provided query."""
        logger.info(f"Fetching papers for query: {query}")
        
        # Simulate fetching papers (you can replace this with actual logic to fetch papers)
        papers = [
            f"Paper 1 on {query}",
            f"Paper 2 on {query}",
            f"Paper 3 on {query}",
        ]
        
        logger.info(f"Found {len(papers)} papers for query: {query}")
        return papers
