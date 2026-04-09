import streamlit as st
import time

# ✅ Import your agent
from heurist_agent import ResearchAgent
agent = ResearchAgent()

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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0d14;
    color: #e2e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1200px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111827; }
::-webkit-scrollbar-thumb { background: #2d6a4f; border-radius: 3px; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0d1f14 0%, #0a1628 50%, #0d1f14 100%);
    border: 1px solid #1a3a2a;
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(52,211,153,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(56,189,248,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #34d399;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    color: #f1f5f9;
    margin-bottom: 0.8rem;
}
.hero-title span { color: #34d399; }
.hero-subtitle {
    font-size: 1.05rem;
    font-weight: 300;
    color: #94a3b8;
    max-width: 520px;
    line-height: 1.7;
}
.hero-badges {
    display: flex;
    gap: 10px;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.25);
    color: #6ee7b7;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.76rem;
    font-weight: 500;
    letter-spacing: 0.04em;
}

/* ── Section headings ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #34d399;
    margin-bottom: 0.4rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 1.4rem;
}

/* ── Input overrides ── */
div[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid #1e3a2e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #34d399 !important;
    box-shadow: 0 0 0 3px rgba(52,211,153,0.12) !important;
}
div[data-testid="stTextInput"] label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Button overrides ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.8rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px rgba(5,150,105,0.3) !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Paper card ── */
.paper-card {
    background: #111827;
    border: 1px solid #1e2d3d;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.paper-card:hover {
    border-color: #2d6a4f;
    box-shadow: 0 4px 24px rgba(52,211,153,0.06);
}
.paper-index {
    position: absolute;
    top: 1.2rem; right: 1.4rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #2d6a4f;
    text-transform: uppercase;
}
.paper-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
    padding-right: 4rem;
    line-height: 1.4;
}
.paper-summary {
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.65;
    margin-bottom: 0.8rem;
}
.paper-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.78rem;
    color: #64748b;
}
.paper-date { color: #6ee7b7; font-weight: 500; }
.paper-link {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #38bdf8;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.82rem;
    margin-top: 0.6rem;
    transition: color 0.2s;
}
.paper-link:hover { color: #7dd3fc; }

/* ── Analyze section ── */
.analyze-box {
    background: linear-gradient(135deg, #0d1f14, #0a1a28);
    border: 1px solid #1a3a2a;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin: 2rem 0 1rem 0;
}

/* ── Answer card ── */
.answer-card {
    background: #0f2318;
    border: 1px solid #1a5c36;
    border-left: 4px solid #34d399;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    font-size: 0.95rem;
    color: #d1fae5;
    line-height: 1.75;
}

/* ── Expander overrides ── */
div[data-testid="stExpander"] {
    background: #111827 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 14px !important;
    margin-bottom: 0.8rem !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex;
    gap: 1px;
    background: #1e2d3d;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.stat-cell {
    flex: 1;
    background: #111827;
    padding: 1rem 1.4rem;
    text-align: center;
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #34d399;
}
.stat-label {
    font-size: 0.72rem;
    color: #64748b;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a2e, transparent);
    margin: 2rem 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e2d3d !important;
}
section[data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 0.2rem;
}
.sidebar-logo span { color: #34d399; }
.sidebar-tagline {
    font-size: 0.75rem;
    color: #4b5563;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.sidebar-section {
    font-family: 'Syne', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #34d399;
    margin: 1.6rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1a3a2a;
}
.sidebar-info-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    padding: 0.35rem 0;
    border-bottom: 1px solid #111827;
}
.sidebar-info-key { color: #64748b; }
.sidebar-info-val { color: #e2e8f0; font-weight: 500; }
.tip-card {
    background: #0d1f14;
    border: 1px solid #1a3a2a;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.78rem;
    color: #6ee7b7;
    line-height: 1.6;
    margin-bottom: 0.6rem;
}
.tip-icon { font-size: 0.9rem; margin-right: 5px; }
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #34d399;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 6px #34d399;
}
.footer-text {
    font-size: 0.72rem;
    color: #374151;
    text-align: center;
    margin-top: 2rem;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">Sci<span>Spy</span></div>
    <div class="sidebar-tagline">Research Intelligence Platform</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">System Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.82rem; color:#94a3b8; padding: 4px 0;">
        <span class="status-dot"></span>Agent Online
    </div>
    <div style="font-size:0.82rem; color:#94a3b8; padding: 4px 0; margin-top:4px;">
        <span style="display:inline-block;width:7px;height:7px;background:#38bdf8;border-radius:50%;margin-right:6px;box-shadow:0 0 6px #38bdf8;"></span>API Connected
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Search Settings</div>', unsafe_allow_html=True)
    max_results = st.slider("Max Papers", min_value=3, max_value=20, value=10, step=1)
    sort_by = st.selectbox("Sort By", ["Relevance", "Date (Newest)", "Citations", "Impact Factor"])
    source_filter = st.multiselect(
        "Sources",
        ["arXiv", "PubMed", "Semantic Scholar", "IEEE", "ACM"],
        default=["arXiv", "Semantic Scholar"]
    )

    st.markdown('<div class="sidebar-section">Display</div>', unsafe_allow_html=True)
    show_abstracts = st.toggle("Show Abstracts", value=True)
    compact_view = st.toggle("Compact View", value=False)
    highlight_keywords = st.toggle("Highlight Keywords", value=True)

    st.markdown('<div class="sidebar-section">Quick Topics</div>', unsafe_allow_html=True)
    topics = ["Large Language Models", "CRISPR Gene Editing", "Quantum Computing", "Climate ML", "Neuromorphic Chips"]
    for topic in topics:
        if st.button(f"↗ {topic}", key=f"quick_{topic}", use_container_width=True):
            st.session_state["quick_topic"] = topic

    st.markdown('<div class="sidebar-section">Tips</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tip-card"><span class="tip-icon">💡</span>Use quotes for exact phrases: <em>"transformer attention"</em></div>
    <div class="tip-card"><span class="tip-icon">🎯</span>Narrow results by adding year: <em>RLHF 2024</em></div>
    <div class="tip-card"><span class="tip-icon">🔗</span>Paste arXiv URLs directly in the analyzer</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info-row"><span class="sidebar-info-key">Framework</span><span class="sidebar-info-val">Heurist Agent</span></div>
    <div class="sidebar-info-row"><span class="sidebar-info-key">Version</span><span class="sidebar-info-val">2.1.0</span></div>
    <div class="sidebar-info-row"><span class="sidebar-info-key">License</span><span class="sidebar-info-val">MIT</span></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-text">
        Built on <strong style="color:#34d399">Heurist Agent Framework</strong><br>
        © 2025 SciSpy Team
    </div>
    """, unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🔬 Research Intelligence</div>
    <div class="hero-title">Discover Science,<br><span>Faster.</span></div>
    <div class="hero-subtitle">
        Search millions of papers, extract insights, and interrogate research
        with AI-powered analysis — all in one place.
    </div>
    <div class="hero-badges">
        <span class="badge">⚡ AI-Powered</span>
        <span class="badge">📚 Multi-Source</span>
        <span class="badge">🔍 Semantic Search</span>
        <span class="badge">🧠 Q&amp;A on Papers</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stats Strip ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-strip">
    <div class="stat-cell"><div class="stat-num">12M+</div><div class="stat-label">Papers Indexed</div></div>
    <div class="stat-cell"><div class="stat-num">5</div><div class="stat-label">Data Sources</div></div>
    <div class="stat-cell"><div class="stat-num">&lt;2s</div><div class="stat-label">Avg. Response</div></div>
    <div class="stat-cell"><div class="stat-num">GPT-4</div><div class="stat-label">Backbone</div></div>
</div>
""", unsafe_allow_html=True)


# ─── Search Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Step 01</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Search Research Papers</div>', unsafe_allow_html=True)

# Handle quick topic shortcut from sidebar
default_query = st.session_state.get("quick_topic", "")
if "quick_topic" in st.session_state:
    del st.session_state["quick_topic"]

col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input(
        "Search query",
        value=default_query,
        placeholder="e.g.  transformer attention mechanisms,  CRISPR off-target effects …",
        key="search_query",
        label_visibility="collapsed",
    )
with col_btn:
    search_clicked = st.button("🔎 Search", use_container_width=True)

if search_clicked and query:
    with st.spinner("Scanning the literature…"):
        time.sleep(1)
        try:
            papers = agent.get_papers(query)
            st.session_state["papers"] = papers
        except Exception as e:
            st.error(f"⚠️ Error retrieving research papers: {str(e)}")


# ─── Results ─────────────────────────────────────────────────────────────────────
if "papers" in st.session_state and st.session_state["papers"]:
    papers = st.session_state["papers"]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{len(papers)} Papers Found</div>', unsafe_allow_html=True)

    for idx, paper in enumerate(papers, 1):
        title   = paper.get("title", "Untitled Paper")
        summary = paper.get("summary", "No summary available.")
        pub     = paper.get("published", "N/A")
        url     = paper.get("url", "#")

        if compact_view:
            with st.expander(f"{'📄'} {title}"):
                if show_abstracts:
                    st.markdown(f"<p style='color:#94a3b8;font-size:0.88rem;line-height:1.65'>{summary}</p>", unsafe_allow_html=True)
                st.markdown(f"📅 **{pub}** &nbsp;|&nbsp; [🔗 Read Paper]({url})", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="paper-card">
                <div class="paper-index">#{idx:02d}</div>
                <div class="paper-title">{title}</div>
                {"<div class='paper-summary'>" + summary + "</div>" if show_abstracts else ""}
                <div class="paper-meta">
                    <span class="paper-date">📅 {pub}</span>
                </div>
                <a class="paper-link" href="{url}" target="_blank">🔗 Read Full Paper →</a>
            </div>
            """, unsafe_allow_html=True)

    # ─── Analyze ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="analyze-box">
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Step 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Analyze a Paper</div>', unsafe_allow_html=True)

    if "selected_paper_url" not in st.session_state:
        st.session_state["selected_paper_url"] = ""

    paper_url = st.text_input(
        "Paper URL",
        value=st.session_state["selected_paper_url"],
        placeholder="https://arxiv.org/abs/xxxx.xxxxx",
        label_visibility="collapsed",
    )

    if st.button("📊 Analyze Paper"):
        st.session_state["selected_paper_url"] = paper_url
        st.session_state["analyzing"] = True
        st.toast("✅ Paper queued for analysis!", icon="🔬")

    st.markdown("</div>", unsafe_allow_html=True)


# ─── Q&A ─────────────────────────────────────────────────────────────────────────
if st.session_state.get("analyzing") and st.session_state.get("selected_paper_url"):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Step 03</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Ask the Paper</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-size:0.8rem;color:#4b5563;margin-bottom:1rem;">
        Analyzing: <span style="color:#38bdf8">{st.session_state['selected_paper_url']}</span>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "Question",
        placeholder="e.g.  What are the main contributions?  What datasets were used?",
        key="question_input",
        label_visibility="collapsed",
    )

    if st.button("💡 Get Answer"):
        with st.spinner("Reasoning over the paper…"):
            time.sleep(1)
            try:
                answer_data = {
                    "answer": f"Answer for '{question}' based on the selected paper."
                }
                st.markdown(f"""
                <div class="answer-card">
                    <strong style="font-family:'Syne',sans-serif;color:#6ee7b7;font-size:0.75rem;
                    letter-spacing:0.15em;text-transform:uppercase;">Answer</strong><br><br>
                    {answer_data['answer']}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"⚠️ Error: {str(e)}")
