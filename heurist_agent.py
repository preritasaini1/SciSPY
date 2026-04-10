import logging
import arxiv
from typing import List
import google.generativeai as genai
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResearchAgent:
    def __init__(self):
        self.agent_name = "ResearchAgent"

        # ✅ Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

        logger.info(f"{self.agent_name} initialized.")

    # 🔥 STEP 2: SMART QUERY REFINEMENT
    def refine_query(self, query: str) -> str:
        try:
            prompt = f"""
            Convert this into a precise academic research search query.
            Focus on the correct domain and context.

            Query: {query}
            """

            response = self.model.generate_content(prompt)

            refined = response.text.strip()
            logger.info(f"Refined query: {refined}")

            return refined if refined else query

        except Exception as e:
            logger.error(f"Gemini refinement failed: {e}")
            return query  # fallback

    # 🔍 MAIN FUNCTION
    def get_papers(self, query: str):
        # ✅ refine query using Gemini
        refined_query = self.refine_query(query)

        search = arxiv.Search(
            query=refined_query,
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
