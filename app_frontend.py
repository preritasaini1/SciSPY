import streamlit as st
import time

# 👉 IMPORT YOUR LOGIC HERE
from heurist_agent import search_papers, answer_query   # adjust if names differ

st.set_page_config(page_title="SciSpy Research Assistant", layout="wide")

st.title("🧑‍🔬 SciSpy Research Assistant")
st.write("🚀 Explore research papers and find answers to your queries.")

# 🔍 Search for research papers
query = st.text_input("🔍 **Search for research papers** (e.g., AI, Quantum Computing)", key="search_query")

if st.button("🔎 Search") and query:
    with st.spinner("Fetching research papers..."):
        time.sleep(1)

        try:
            papers = search_papers(query)   # ✅ direct call
            st.session_state["papers"] = papers
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# 🔎 Display search results
if "papers" in st.session_state and st.session_state["papers"]:
    st.subheader("📑 **Search Results**")
    
    for idx, paper in enumerate(st.session_state["papers"], 1):
        with st.expander(f"📄 {paper.get('title', 'No Title')}"):
            st.write(f"**Summary:** {paper.get('summary', 'No summary')}")
            st.write(f"📅 **Published:** {paper.get('published', 'N/A')}")
            st.markdown(f"🔗 [**Read Full Paper**]({paper.get('url', '#')})")

    # 🎯 Paper URL input
    st.subheader("📥 **Analyze a Research Paper**")
    
    if "selected_paper_url" not in st.session_state:
        st.session_state["selected_paper_url"] = ""

    paper_url = st.text_input("🔗 **Enter the paper URL:**", value=st.session_state["selected_paper_url"])

    if st.button("📊 Analyze Paper"):
        st.session_state["selected_paper_url"] = paper_url
        st.session_state["analyzing"] = True
        st.toast("✅ Paper URL submitted!")

# 🧐 Q&A Section
if st.session_state.get("analyzing") and st.session_state.get("selected_paper_url"):
    st.subheader("🧐 **Ask a Question about the Paper**")
    
    question = st.text_input("❓ **Type your question here:**", key="question_input")

    if st.button("💡 Get Answer"):
        with st.spinner("🔍 Generating answer..."):
            time.sleep(1)

            try:
                answer = answer_query(st.session_state["selected_paper_url"], question)
                st.success(f"💡 **Answer:** {answer}")
            except Exception as e:
                st.warning(f"⚠️ Error: {str(e)}")

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
