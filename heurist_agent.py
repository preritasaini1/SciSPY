import logging
import arxiv
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

    # 🔥 SMART QUERY REFINEMENT (FIXED)
    def refine_query(self, query: str) -> str:
        try:
            prompt = f"""
            Convert the following query into a SHORT academic search query (max 10 words).

            DO NOT explain.
            DO NOT give multiple options.
            ONLY return the final query.

            Query: {query}
            """

            response = self.model.generate_content(prompt)

            refined = response.text.strip()

            # ✅ safety cleaning
            refined = refined.split("\n")[0]
            refined = refined[:100]
            refined = refined.replace('"', '').replace("'", "")

            logger.info(f"Refined query: {refined}")

            return refined if refined else query

        except Exception as e:
            logger.error(f"Gemini refinement failed: {e}")
            return query

    # 🔍 MAIN FUNCTION
    def get_papers(self, query: str):
        refined_query = self.refine_query(query)

        search = arxiv.Search(
            query=refined_query,
            max_results=10,  # 🔥 get more for better ranking
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

        # 🔥 BOOST IMPORTANT ML PAPERS
        priority_keywords = [
            "attention is all you need",
            "transformer",
            "bert",
            "gpt",
            "self-attention"
        ]

        papers = sorted(
            papers,
            key=lambda p: any(k in p["title"].lower() for k in priority_keywords),
            reverse=True
        )

        # ✅ return top 5
        return papers[:5]
