import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"  # Update if needed

st.set_page_config(page_title="SciSpy Research Assistant", layout="wide")

st.title("🧑‍🔬 SciSpy Research Assistant")
st.write("🚀 Explore research papers and find answers to your queries.")

# 🔍 Search for research papers
query = st.text_input("🔍 **Search for research papers** (e.g., AI, Quantum Computing)", key="search_query")

if st.button("🔎 Search") and query:
    with st.spinner("Fetching research papers..."):
        response = requests.post(f"{API_URL}/search_papers/", json={"query": query})
        time.sleep(1)  # Simulating loading effect

        if response.status_code == 200:
            data = response.json()
            st.session_state["papers"] = data["papers"]  # Store results in session state
        else:
            st.error("⚠️ Error retrieving research papers. Please try again.")

# 🔎 Display search results (persistent across interactions)
if "papers" in st.session_state and st.session_state["papers"]:
    st.subheader("📑 **Search Results**")
    
    for idx, paper in enumerate(st.session_state["papers"], 1):
        with st.expander(f"📄 {paper['title']}"):
            st.write(f"**Summary:** {paper['summary']}")
            st.write(f"📅 **Published:** {paper['published']}")
            st.markdown(f"🔗 [**Read Full Paper**]({paper['url']})", unsafe_allow_html=True)

    # 🎯 Paper URL input section
    st.subheader("📥 **Analyze a Research Paper**")
    
    if "selected_paper_url" not in st.session_state:
        st.session_state["selected_paper_url"] = ""  # Ensure persistence

    paper_url = st.text_input("🔗 **Enter the paper URL:**", value=st.session_state["selected_paper_url"])

    if st.button("📊 Analyze Paper"):
        st.session_state["selected_paper_url"] = paper_url
        st.session_state["analyzing"] = True
        st.toast("✅ **Paper URL submitted for analysis!**")

# 🧐 **Question & Answer Section**
if st.session_state.get("analyzing") and st.session_state.get("selected_paper_url"):
    st.subheader("🧐 **Ask a Question about the Paper**")
    
    question = st.text_input("❓ **Type your question here:**", key="question_input")

    if st.button("💡 Get Answer"):
        with st.spinner("🔍 Generating answer..."):
            response = requests.post(
                f"{API_URL}/answer_query/", 
                json={"url": st.session_state["selected_paper_url"], "query": question}
            )
            time.sleep(1)  # Simulating processing delay

            if response.status_code == 200:
                answer_data = response.json()
                st.success(f"💡 **Answer:** {answer_data['answer']}")
            else:
                st.warning("⚠️ Error retrieving answer. Please try again.")

# 🎨 **Enhancements**
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
        </style>
        """, unsafe_allow_html=True
    )

st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 Developed by **SciSpy Team** | 🚀 Powered by AI")

