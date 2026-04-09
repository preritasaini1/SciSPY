import google.generativeai as genai
import requests
import arxiv
import fitz  # PyMuPDF
import logging
from typing import Dict, Any

# Configure logging and Gemini
logging.basicConfig(level=logging.INFO)
GEMINI_API_KEY = "AIzaSyAbyZguUXue50Unx0Mgvebj_vmLJMHq358"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class ResearchAgent:
    def __init__(self):
        self.pdf_content = None
        
    async def fetch_papers(self, topic, max_results=5):
        try:
            search = arxiv.Search(
                query=topic,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending,
            )
            
            papers = []
            for result in search.results():
                paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary[:300] + "...",  # Shorter summary
                "url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d") if result.published else "Unknown"
            }
                papers.append(paper)
            return papers
            
        except Exception as e:
            logging.error(f"Error fetching papers: {str(e)}")
            return []

    async def extract_pdf_content(self, url):
        try:
            response = requests.get(url)
            pdf_bytes = response.content
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            text = ""
            for page_num in range(min(5, pdf_document.page_count)):  # First 5 pages
                page = pdf_document.load_page(page_num)
                text += page.get_text()

            self.pdf_content = text  # Store for future use
            return text  # Return extracted text
        
        except Exception as e:
            logging.error(f"Error extracting PDF: {str(e)}")
            return None


    async def answer_query(self, pdf_text, query):
        if not pdf_text:
            return "No content found in the paper. Please check the PDF URL."

        try:
            prompt = f"""
            Based on the following research paper content:
            {pdf_text[:10000]}
            
            Question: {query}
            
            Please provide a clear and concise answer based on the paper content.
            """

            response = model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            logging.error(f"Error generating answer: {str(e)}")
            return f"Error generating answer: {str(e)}"
