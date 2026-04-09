# test_mesh_research_agent.py
import asyncio
from mesh.research_agent import ResearchAgent


async def interactive_research():
    agent = ResearchAgent()
    
    # Get topic from user
    topic = input("Enter research topic to search: ")
    
    # Fetch papers
    papers = await agent.fetch_papers(topic)
    
    if not papers:
        print("No papers found!")
        return
        
    # Display papers
    print("\nFetched Papers:")
    for idx, paper in enumerate(papers, 1):
        print(f"\n{idx}. Title: {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'])}")
        print(f"   Summary: {paper['summary']}")
        print(f"   URL: {paper['url']}")
        print(f"   Published: {paper['published']}")

    
    # Get URL choice from user
    while True:
        chosen_url = input("\nPaste the URL of the paper you want to analyze (or 'quit' to exit): ")
        if chosen_url.lower() == 'quit':
            break
            
        # Load the chosen paper
        print("\nLoading paper...")
        success = await agent.extract_pdf_content(chosen_url)
        
        if success:
            print("Paper loaded successfully! You can now ask questions.")
            
            # Question-answering loop
            while True:
                question = input("\nEnter your question about the paper (or 'quit' to exit): ")
                if question.lower() == 'quit':
                    break
                    
                print("\nGenerating answer...")
                answer = await agent.answer_query(question)
                print(f"\nAnswer: {answer}")
        else:
            print("Failed to load paper. Please check the URL and try again.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(interactive_research())