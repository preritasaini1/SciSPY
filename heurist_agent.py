import logging
import arxiv
import google.generativeai as genai
import os

# 🔧 Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResearchAgent:
    def __init__(self):
        self.agent_name = "ResearchAgent"

        # 🔐 Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

        logger.info(f"{self.agent_name} initialized.")

    # 🔥 SMART QUERY REFINEMENT (CONTROLLED OUTPUT)
    def refine_query(self, query: str) -> str:
        try:
            prompt = f"""
            Convert this into a SHORT academic search query (max 10 words).

            DO NOT explain.
            ONLY return the query.

            Query: {query}
            """

            response = self.model.generate_content(prompt)

            refined = response.text.strip()

            # ✅ Clean output
            refined = refined.split("\n")[0]
            refined = refined[:100]
            refined = refined.replace('"', '').replace("'", "")

            logger.info(f"Refined query: {refined}")

            return refined if refined else query

        except Exception as e:
            logger.error(f"Gemini refinement failed: {e}")
            return query

    # 🔍 MAIN SEARCH FUNCTION
    def get_papers(self, query: str):
        refined_query = self.refine_query(query)

        search = arxiv.Search(
            query=refined_query,
            max_results=15,  # larger pool for ranking
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

        # 🔥 SMART RANKING SYSTEM
        def score(p):
            title = p["title"].lower()
            summary = p["summary"].lower()

            s = 0

            # ⭐ Importance boost (famous concepts)
            important_terms = [
                "transformer",
                "bert",
                "gpt",
                "attention is all you need",
                "neural",
                "deep learning",
                "foundation model"
            ]

            s += sum(term in title for term in important_terms) * 3

            # ⭐ Query relevance
            query_words = query.lower().split()
            s += sum(word in title for word in query_words) * 2
            s += sum(word in summary for word in query_words)

            # ⭐ Slight boost for older influential papers
            try:
                year = int(p["published"][:4])
                if year < 2018:
                    s += 1
            except:
                pass

            return s

        # 🔥 Sort by score
        papers = sorted(papers, key=score, reverse=True)

        # ✅ Return top 5
        return papers[:5]
