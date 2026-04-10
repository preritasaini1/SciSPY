import logging
import arxiv
import requests

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchAgent:
    def __init__(self):
        self.agent_name = "ResearchAgent"
        logger.info(f"{self.agent_name} initialized.")

    # 🔹 Semantic Scholar API
    def fetch_semantic_scholar(self, query, max_results):
        url = "https://api.semanticscholar.org/graph/v1/paper/search"

        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,abstract,year,url"
        }

        try:
            res = requests.get(url, params=params)
            data = res.json()

            papers = []
            for p in data.get("data", []):
                papers.append({
                    "title": p.get("title"),
                    "summary": (p.get("abstract") or "")[:300] + "...",
                    "published": str(p.get("year")),
                    "url": p.get("url")
                })

            return papers

        except Exception as e:
            logger.error(f"Semantic Scholar error: {e}")
            return []

    # 🔍 MAIN FUNCTION
    def get_papers(self, query: str, max_results=5, sort_by="Relevance", sources=None):
        logger.info(f"Fetching papers for query: {query}")

        papers = []

        # 🔹 ARXIV
        if not sources or "arXiv" in sources:

            if sort_by == "Date (Newest)":
                sort = arxiv.SortCriterion.SubmittedDate
            else:
                sort = arxiv.SortCriterion.Relevance

            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort
            )

            for result in search.results():
                papers.append({
                    "title": result.title,
                    "summary": result.summary[:300] + "...",
                    "published": str(result.published.date()),
                    "url": result.entry_id
                    "pdf_url": result.pdf_url
                })

        # 🔹 SEMANTIC SCHOLAR
        if sources and "Semantic Scholar" in sources:
            papers += self.fetch_semantic_scholar(query, max_results)

        # 🔥 REMOVE DUPLICATES (based on title)
        unique = {}
        for p in papers:
            if p["title"]:
                unique[p["title"]] = p

        papers = list(unique.values())

        # 🔥 FINAL LIMIT
        return papers[:max_results]
