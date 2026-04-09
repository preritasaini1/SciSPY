import streamlit as st
import time

# ✅ import your class
from heurist_agent import ResearchAgent

# ✅ create object
agent = ResearchAgent()

st.set_page_config(page_title="SciSpy Research Assistant", layout="wide")

st.title("🧑‍🔬 SciSpy Research Assistant")
st.write("🚀 Explore research papers and find answers to your queries.")

# 🔍 Search
query = st.text_input("🔍 **Search for research papers** (e.g., AI, Quantum Computing)")

if st.button("🔎 Search") and query:
    with st.spinner("Fetching research papers..."):
        time.sleep(1)

        try:
            papers = agent.get_papers(query)   # ✅ correct call

            # convert to UI-friendly format
            st.session_state["papers"] = [
                {
                    "title": paper,
                    "summary": "Sample summary",
                    "published": "N/A",
                    "url": "#"
                }
                for paper in papers
            ]

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# 🔎 Display results
if "papers" in st.session_state and st.session_state["papers"]:
    st.subheader("📑 **Search Results**")

    for paper in st.session_state["papers"]:
        with st.expander(f"📄 {paper['title']}"):
            st.write(f"**Summary:** {paper['summary']}")
            st.write(f"📅 **Published:** {paper['published']}")
            st.markdown(f"🔗 [Read Paper]({paper['url']})")

# 🎨 Sidebar
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("🎨 Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown(
        """
        <style>
            body {
                background-color: #1e1e1e;
                color: white;
            }
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 Developed by **SciSpy Team** | 🚀 Powered by AI")
