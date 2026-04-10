import streamlit as st
import time
import os
import google.generativeai as genai

# ✅ Import your agent
from heurist_agent import ResearchAgent
agent = ResearchAgent()

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SciSpy · Research Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Sans+3:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #f8f5f0;
    color: #2c2825;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3.5rem 5rem 3.5rem; max-width: 1100px; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #ede8e0; }
::-webkit-scrollbar-thumb { background: #b8a898; border-radius: 3px; }

/* ── Masthead ── */
.masthead {
    border-top: 3px solid #2c2825;
    border-bottom: 1px solid #d4cfc8;
    padding: 1.4rem 0 1.2rem 0;
    margin-bottom: 2rem;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.masthead-title {
    font-family: 'Lora', serif;
    font-size: 1.8rem;
    font-weight: 600;
    font-style: italic;
    color: #2c2825;
}
.masthead-title span { font-style: normal; color: #1a6b3a; }
.masthead-meta {
    font-size: 0.72rem;
    color: #9c9488;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

/* ── Intro ── */
.intro-blurb {
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    color: #4a453f;
    line-height: 1.8;
    max-width: 640px;
    margin-bottom: 0.5rem;
}
.intro-blurb em { color: #1a6b3a; }

.tag-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 0.8rem 0 1.8rem 0; }
.tag {
    border: 1px solid #c8c0b4;
    border-radius: 3px;
    padding: 2px 9px;
    font-size: 0.69rem;
    color: #6b6358;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    background: transparent;
}

/* ── Dividers ── */
.rule { height: 1px; background: #d4cfc8; margin: 1.8rem 0; }
.rule-double { border-top: 3px double #c8c0b4; margin: 2rem 0; }

/* ── Section ── */
.sec-eyebrow {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #9c9488;
    margin-bottom: 0.25rem;
}
.sec-heading {
    font-family: 'Lora', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #2c2825;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e0dbd3;
    padding-bottom: 0.45rem;
}

/* ── Stats ── */
.stats-row {
    display: flex;
    border: 1px solid #d4cfc8;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.stat-cell {
    flex: 1;
    padding: 0.85rem 1rem;
    border-right: 1px solid #d4cfc8;
    background: #fff;
    text-align: center;
}
.stat-cell:last-child { border-right: none; }
.stat-num { font-family: 'Lora', serif; font-size: 1.2rem; font-weight: 500; color: #1a6b3a; }
.stat-lbl { font-size: 0.62rem; color: #9c9488; letter-spacing: 0.09em; text-transform: uppercase; margin-top: 2px; }

/* ── Inputs ── */
div[data-testid="stTextInput"] input {
    background: #fff !important;
    border: 1px solid #c8c0b4 !important;
    border-radius: 3px !important;
    color: #2c2825 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.58rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #1a6b3a !important;
    box-shadow: 0 0 0 2px rgba(26,107,58,0.08) !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #b0a898 !important; }
div[data-testid="stTextInput"] label { color: #6b6358 !important; font-size: 0.8rem !important; }

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    background: #1a6b3a !important;
    color: #f8f5f0 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    padding: 0.56rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: none !important;
    transition: background 0.18s !important;
}
div[data-testid="stButton"] > button:hover { background: #145530 !important; }

/* ── Paper card ── */
.paper-card {
    background: #fff;
    border: 1px solid #d4cfc8;
    border-left: 3px solid #1a6b3a;
    border-radius: 3px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: box-shadow 0.18s;
}
.paper-card:hover { box-shadow: 0 2px 10px rgba(44,40,37,0.07); }
.paper-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #9c9488;
    margin-bottom: 0.3rem;
}
.paper-title {
    font-family: 'Lora', serif;
    font-size: 0.98rem;
    font-weight: 600;
    color: #2c2825;
    line-height: 1.45;
    margin-bottom: 0.5rem;
}
.paper-abstract {
    font-size: 0.84rem;
    color: #5c5850;
    line-height: 1.7;
    margin-bottom: 0.65rem;
    font-style: italic;
}
.paper-footer { display: flex; justify-content: space-between; align-items: center; }
.paper-date { font-size: 0.74rem; color: #9c9488; }
.paper-link {
    font-size: 0.76rem;
    font-weight: 600;
    color: #1a6b3a;
    text-decoration: none;
    border-bottom: 1px solid rgba(26,107,58,0.35);
}
.paper-link:hover { border-color: #1a6b3a; }

/* ── Analyze box ── */
.analyze-box {
    background: #faf7f2;
    border: 1px solid #d4cfc8;
    border-radius: 3px;
    padding: 1.3rem 1.6rem;
}

/* ── Answer ── */
.answer-box {
    background: #f0f7f3;
    border: 1px solid #b8d8c4;
    border-left: 3px solid #1a6b3a;
    border-radius: 3px;
    padding: 1.1rem 1.4rem;
    margin-top: 1rem;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 0.92rem;
    color: #2c3e30;
    line-height: 1.75;
}
.answer-label {
    font-family: 'Source Sans 3', sans-serif;
    font-style: normal;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1a6b3a;
    margin-bottom: 0.45rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #f0ece4 !important;
    border-right: 1px solid #d4cfc8 !important;
}
.sb-logo {
    font-family: 'Lora', serif;
    font-size: 1.2rem;
    font-weight: 600;
    font-style: italic;
    color: #2c2825;
    padding-top: 0.2rem;
}
.sb-logo span { font-style: normal; color: #1a6b3a; }
.sb-sub {
    font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: #9c9488; margin-bottom: 1.4rem; font-weight: 500;
}
.sb-sec {
    font-size: 0.58rem; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #6b6358;
    border-bottom: 1px solid #c8c0b4;
    padding-bottom: 0.35rem; margin: 1.3rem 0 0.8rem 0;
}
.st-row { display: flex; align-items: center; gap: 7px; font-size: 0.79rem; color: #5c5850; margin-bottom: 4px; }
.dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.dot-g { background: #1a6b3a; }
.dot-b { background: #2563eb; }
.tip { font-size: 0.77rem; color: #6b6358; line-height: 1.6; padding: 0.45rem 0; border-bottom: 1px dashed #d4cfc8; }
.tip:last-child { border-bottom: none; }
.mr { display: flex; justify-content: space-between; font-size: 0.77rem; padding: 0.28rem 0; border-bottom: 1px solid #e0dbd3; }
.mk { color: #9c9488; }
.mv { color: #2c2825; font-weight: 500; }
.sb-foot {
    font-size: 0.68rem; color: #b0a898; text-align: center;
    margin-top: 1.8rem; line-height: 1.7;
    border-top: 1px solid #d4cfc8; padding-top: 0.9rem;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #fff !important;
    border: 1px solid #d4cfc8 !important;
    border-left: 3px solid #1a6b3a !important;
    border-radius: 3px !important;
    margin-bottom: 0.7rem !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Lora', serif !important;
    font-size: 0.93rem !important;
    font-weight: 600 !important;
    color: #2c2825 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">Sci<span>Spy</span></div><div class="sb-sub">Research Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">System Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="st-row"><span class="dot dot-g"></span>Agent Online</div>
    <div class="st-row"><span class="dot dot-b"></span>API Connected</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Search Settings</div>', unsafe_allow_html=True)
    max_results = st.slider("Max papers", min_value=3, max_value=20, value=10)
    sort_by = st.selectbox("Sort by", ["Relevance", "Date (Newest)", "Citations", "Impact Factor"])
    source_filter = st.multiselect("Sources", ["arXiv", "PubMed", "Semantic Scholar", "IEEE", "ACM"], default=["arXiv", "Semantic Scholar"])

    st.markdown('<div class="sb-sec">Display</div>', unsafe_allow_html=True)
    show_abstracts = st.toggle("Show abstracts", value=True)
    compact_view   = st.toggle("Compact view", value=False)

    st.markdown('<div class="sb-sec">Quick Search</div>', unsafe_allow_html=True)
    quick_topics = ["Large Language Models", "CRISPR Gene Editing", "Quantum Computing",
                    "Climate ML", "Neuromorphic Chips", "Protein Folding", "Federated Learning"]
    for topic in quick_topics:
        if st.button(f"↗ {topic}", key=f"qt_{topic}", use_container_width=True):
            st.session_state["quick_topic"] = topic

    st.markdown('<div class="sb-sec">Search Tips</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tip">💬 Quotes for exact phrases: <em>"attention mechanism"</em></div>
    <div class="tip">📅 Add year to narrow: <em>RLHF 2024</em></div>
    <div class="tip">🔗 Paste arXiv URLs in the analyzer</div>
    <div class="tip">🧑‍🔬 Combine field + method: <em>genomics transformer</em></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="mr"><span class="mk">Framework</span><span class="mv">Heurist Agent</span></div>
    <div class="mr"><span class="mk">Version</span><span class="mv">2.1.0</span></div>
    <div class="mr"><span class="mk">License</span><span class="mv">MIT</span></div>
    <div class="mr"><span class="mk">Indexed</span><span class="mv">12M+ papers</span></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-foot">Built on <strong>Heurist Agent Framework</strong><br>© 2025 SciSpy Team</div>', unsafe_allow_html=True)


# ─── Masthead ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-title"><em>Sci</em><span>Spy</span> Research Intelligence</div>
    <div class="masthead-meta">Heurist Agent · Vol. 2 · 2025</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p class="intro-blurb">
    Search across millions of peer-reviewed papers, preprints, and technical reports.
    Surface insights with <em>AI-assisted analysis</em> — and interrogate any paper with natural language.
</p>
<div class="tag-row">
    <span class="tag">Semantic Search</span>
    <span class="tag">AI Q&amp;A</span>
    <span class="tag">Multi-Source</span>
    <span class="tag">arXiv · PubMed · Semantic Scholar</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-cell"><div class="stat-num">12M+</div><div class="stat-lbl">Papers Indexed</div></div>
    <div class="stat-cell"><div class="stat-num">5</div><div class="stat-lbl">Sources</div></div>
    <div class="stat-cell"><div class="stat-num">&lt;2s</div><div class="stat-lbl">Avg. Response</div></div>
    <div class="stat-cell"><div class="stat-num">GPT-4</div><div class="stat-lbl">Backbone</div></div>
</div>
""", unsafe_allow_html=True)


# ─── Search ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-eyebrow">Step 01</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-heading">Search the Literature</div>', unsafe_allow_html=True)

default_query = st.session_state.pop("quick_topic", "")
col_q, col_btn = st.columns([5, 1])
with col_q:
    query = st.text_input("query", value=default_query,
        placeholder="e.g.  transformer attention mechanisms,  CRISPR off-target effects …",
        key="search_query", label_visibility="collapsed")
with col_btn:
    search_clicked = st.button("Search →", use_container_width=True)

if search_clicked and query:
    with st.spinner("Scanning the literature…"):
        time.sleep(1)
        try:
            papers = agent.get_papers(
                query,
                max_results=max_results,
                sort_by=sort_by,
                sources=source_filter
            )
            st.session_state["papers"] = papers
        except Exception as e:
            st.error(f"Error: {str(e)}")


# ─── Results ─────────────────────────────────────────────────────────────────────
if "papers" in st.session_state and st.session_state["papers"]:
    papers = st.session_state["papers"]
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-heading">{len(papers)} papers found</div>', unsafe_allow_html=True)

    for idx, paper in enumerate(papers, 1):
        title   = paper.get("title", "Untitled")
        summary = paper.get("summary", "No abstract available.")
        pub     = paper.get("published", "n.d.")
        url     = paper.get("url", "#")

        if compact_view:
            with st.expander(title):
                if show_abstracts:
                    st.markdown(f"<p class='paper-abstract'>{summary}</p>", unsafe_allow_html=True)
                st.markdown(f"Published: **{pub}** · [Read paper →]({url})", unsafe_allow_html=True)
        else:
            abs_html = f'<div class="paper-abstract">{summary}</div>' if show_abstracts else ""
            st.markdown(f"""
            <div class="paper-card">
                <div class="paper-num">[{idx:02d}] · {pub}</div>
                <div class="paper-title">{title}</div>
                {abs_html}
                <div class="paper-footer">
                    <span class="paper-date"></span>
                    <a class="paper-link" href="{url}" target="_blank">Read full paper →</a>
                    &nbsp;&nbsp;
                    <a class="paper-link" href="{pdf_url}" target="_blank">📄 PDF</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Analyze ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="rule-double"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">Step 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Analyze a Paper</div>', unsafe_allow_html=True)

    st.markdown('<div class="analyze-box">', unsafe_allow_html=True)
    if "selected_paper_url" not in st.session_state:
        st.session_state["selected_paper_url"] = ""

    paper_url = st.text_input("url", value=st.session_state["selected_paper_url"],
        placeholder="https://arxiv.org/abs/xxxx.xxxxx", label_visibility="collapsed")
    if st.button("Analyze →"):
        st.session_state["selected_paper_url"] = paper_url
        st.session_state["analyzing"] = True
        st.toast("Paper queued for analysis.", icon="🔬")
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Q&A ─────────────────────────────────────────────────────────────────────────
if st.session_state.get("analyzing") and st.session_state.get("selected_paper_url"):
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">Step 03</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Ask a Question</div>', unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.75rem;color:#9c9488;font-family:\'JetBrains Mono\',monospace;margin-bottom:0.9rem;">{st.session_state["selected_paper_url"]}</div>', unsafe_allow_html=True)

    question = st.text_input("Question", placeholder="e.g.  What is the main contribution?  Which dataset was used?",
        key="question_input", label_visibility="collapsed")

    if st.button("Get Answer →"):
        with st.spinner("Reading the paper…"):
            try:
                import arxiv
    
                paper_url = st.session_state["selected_paper_url"]
    
                # 🔥 Extract paper ID from URL
                paper_id = paper_url.split("/")[-1]
    
                # 🔥 Fetch real paper data
                search = arxiv.Search(id_list=[paper_id])
                result = next(search.results())
    
                summary = result.summary
    
                # 🔥 Give ACTUAL content to Gemini
                prompt = f"""
                You are a research assistant.
    
                Use ONLY the following research paper summary to answer.
    
                Paper Summary:
                {summary}
    
                Question:
                {question}
    
                If answer is not present, say "Not mentioned in paper".
                """
    
                response = gemini_model.generate_content(prompt)
    
                if response.candidates:
                    st.markdown(f"""
                    <div class="answer-box">
                        <div class="answer-label">Answer</div>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No response generated.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
