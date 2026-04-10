import logging
import arxiv

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.agent_name = "ResearchAgent"
        logger.info(f"{self.agent_name} initialized.")

    def get_papers(self, query: str):
        logger.info(f"Fetching papers for query: {query}")

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
                "url": result.entry_id
            })

        return papers
