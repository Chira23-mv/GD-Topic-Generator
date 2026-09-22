import streamlit as st

st.set_page_config(page_title="GD Topic Generator", page_icon="🗣️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f3f7ff;
        --bg-strong: #eef3ff;
        --panel: rgba(255,255,255,0.82);
        --panel-strong: #ffffff;
        --border: rgba(99, 102, 241, 0.14);
        --text: #0f172a;
        --muted: #52607a;
        --primary: #4338ca;
        --primary-strong: #312e81;
        --secondary: #0ea5e9;
        --accent: #8b5cf6;
        --soft-primary: rgba(67, 56, 202, 0.12);
        --shadow: 0 24px 60px rgba(15, 23, 42, 0.10);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(99, 102, 241, 0.18), transparent 28%),
            radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.15), transparent 30%),
            linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
        max-width: 1360px;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }

    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 12px 18px;
        margin-bottom: 16px;
        border: 1px solid var(--border);
        border-radius: 999px;
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
    }

    .nav-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 14px;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(67, 56, 202, 0.12), rgba(14, 165, 233, 0.12));
        color: var(--primary);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        box-shadow: inset 0 0 0 1px rgba(67, 56, 202, 0.08);
    }

    .kicker {
        color: var(--muted);
        font-weight: 700;
        letter-spacing: 0.02em;
        font-size: 0.82rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(239,245,255,0.96) 100%);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 32px;
        padding: 30px 28px;
        box-shadow: var(--shadow);
        margin-bottom: 18px;
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -60px;
        top: -30px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,0.18), rgba(99,102,241,0));
        pointer-events: none;
    }

    .hero h1 {
        margin-bottom: 12px;
        line-height: 0.96;
        letter-spacing: -0.06em;
        font-size: clamp(2.4rem, 4vw, 4rem);
    }

    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 14px;
        color: var(--primary);
        font-weight: 800;
        font-size: 0.92rem;
    }

    .feature-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(250,252,255,0.96) 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 22px 20px;
        box-shadow: 0 18px 32px rgba(15, 23, 42, 0.04);
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        border-color: rgba(67, 56, 202, 0.18);
        box-shadow: 0 24px 36px rgba(67, 56, 202, 0.09);
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 18px 0 10px;
    }

    .metric-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(244,247,255,0.97) 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 18px 18px 16px;
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.03);
    }

    .metric-box strong {
        display: inline-block;
        font-size: 1.7rem;
        line-height: 1;
        color: var(--text);
        margin-bottom: 6px;
    }

    .metric-box span {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .section-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(67, 56, 202, 0.10), rgba(14, 165, 233, 0.10));
        color: var(--primary-strong);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .stButton > button {
        border-radius: 16px;
        font-weight: 800;
        padding: 0.7rem 1.2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        box-shadow: 0 16px 26px rgba(67, 56, 202, 0.22);
        transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
    }

    .stButton > button:hover {
        filter: brightness(1.04);
        transform: translateY(-1px);
        box-shadow: 0 20px 28px rgba(67, 56, 202, 0.24);
    }

    .soft-text {
        color: var(--muted);
        line-height: 1.7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="top-nav"><div class="nav-badge">GD Spark</div><div class="kicker">Smart group discussion prep</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hero">', unsafe_allow_html=True)
left_col, right_col = st.columns([1.35, 1])
with left_col:
    st.title("🗣️ GD Topic Generator")
    st.caption("Smart discussion topics, stronger structure, and a cleaner path to confident speaking.")
    st.write("Discover fresh GD prompts, filter by category, and move into a focused prep view with balanced arguments and practical talking points.")
    st.markdown("<div class='hero-cta'>⚡ Build better discussion flow</div>", unsafe_allow_html=True)
    if st.button("Start generating topics", type="primary", use_container_width=True):
        st.switch_page("pages/1_Choose_Topic.py")
with right_col:
    st.image(
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
        width=420,
        caption="Brainstorm ideas with clarity",
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="metric-grid">
        <div class="metric-box">
            <strong>5</strong><br>
            <span>fresh topics per batch</span>
        </div>
        <div class="metric-box">
            <strong>5+</strong><br>
            <span>categories to explore</span>
        </div>
        <div class="metric-box">
            <strong>1</strong><br>
            <span>clean prep flow</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-tag'>Why it helps</div>", unsafe_allow_html=True)
features = st.columns(3)
with features[0]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.subheader("1. Explore")
    st.write("Find fresh discussion prompts across current affairs, technology, business, social issues, and abstract thinking.")
    st.markdown("</div>", unsafe_allow_html=True)
with features[1]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.subheader("2. Filter")
    st.write("Choose a category and narrow down the list to the kind of GD you want to prepare for.")
    st.markdown("</div>", unsafe_allow_html=True)
with features[2]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.subheader("3. Prepare")
    st.write("Move into a dedicated prep view with structure, examples, key arguments, and speaking tips.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

info = st.columns([1.2, 1])
with info[0]:
    st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
    st.subheader("What makes it easier")
    st.markdown("• 5 fresh topics at a time<br>• Quick next-batch browsing<br>• Clear GD prep structure<br>• Clean white design with subtle transparency", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with info[1]:
    st.image(
        "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
        width=420,
        caption="Prepared conversations create better confidence",
    )
