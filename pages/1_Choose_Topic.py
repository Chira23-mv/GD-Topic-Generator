import json
import math
import random
import time
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Topic Picker", page_icon="🎯", layout="wide")

TOPICS_FILE = Path(__file__).resolve().parents[1] / "topics.json"


@st.cache_data
def load_topics():
    with open(TOPICS_FILE, encoding="utf-8") as f:
        return json.load(f)


topics = load_topics()
CATEGORY_ICONS = {
    "Current Affairs": "assets/current_affairs.svg",
    "Technology": "assets/technology.svg",
    "Social Issues": "assets/social_issues.svg",
    "Business & Economy": "assets/business_economy.svg",
    "Abstract": "assets/abstract.svg",
}


def get_icon_path(category: str) -> str:
    return CATEGORY_ICONS.get(category, "assets/abstract.svg")


if "category" not in st.session_state:
    st.session_state.category = "All"
if "minutes" not in st.session_state:
    st.session_state.minutes = 2
if "history" not in st.session_state:
    st.session_state.history = []
if "pool" not in st.session_state:
    st.session_state.pool = []
if "page" not in st.session_state:
    st.session_state.page = 0
if "current_candidates" not in st.session_state:
    st.session_state.current_candidates = []
if "topic" not in st.session_state:
    st.session_state.topic = None
if "topic_category" not in st.session_state:
    st.session_state.topic_category = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "total" not in st.session_state:
    st.session_state.total = 0
if "alerted" not in st.session_state:
    st.session_state.alerted = False


def get_topic_pool(selected_category: str):
    if selected_category == "All":
        pool = [(cat, topic) for cat, topic_list in topics.items() for topic in topic_list]
    else:
        pool = [(selected_category, topic) for topic in topics[selected_category]]
    random.shuffle(pool)
    return pool


def reset_topic_pool():
    st.session_state.pool = get_topic_pool(st.session_state.category)
    st.session_state.page = 0
    st.session_state.current_candidates = st.session_state.pool[:5]


def next_batch():
    if not st.session_state.pool:
        reset_topic_pool()
        return
    next_page = st.session_state.page + 1
    start = next_page * 5
    end = start + 5
    if start >= len(st.session_state.pool):
        reset_topic_pool()
        return
    st.session_state.page = next_page
    st.session_state.current_candidates = st.session_state.pool[start:end]


def select_candidate(cat: str, topic: str):
    st.session_state.topic = topic
    st.session_state.topic_category = cat
    st.session_state.end_time = None
    st.session_state.alerted = False
    st.session_state.history = [topic] + [item for item in st.session_state.history if item != topic]
    st.session_state.history = st.session_state.history[:10]
    st.switch_page("pages/2_Prepare_GD.py")


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f3f7ff;
        --panel: rgba(255,255,255,0.86);
        --border: rgba(99, 102, 241, 0.14);
        --text: #0f172a;
        --muted: #52607a;
        --primary: #4338ca;
        --primary-strong: #312e81;
        --secondary: #0ea5e9;
        --soft-primary: rgba(67, 56, 202, 0.10);
        --shadow: 0 24px 60px rgba(15, 23, 42, 0.10);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(67, 56, 202, 0.18), transparent 26%),
            radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.16), transparent 30%),
            linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.4rem;
        max-width: 1360px;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }

    .topbar {
        background: linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(239,245,255,0.96) 100%);
        border: 1px solid var(--border);
        border-radius: 30px;
        padding: 22px 24px;
        margin-bottom: 12px;
        box-shadow: var(--shadow);
    }

    .page-chip {
        display: inline-block;
        background: linear-gradient(135deg, rgba(67, 56, 202, 0.10), rgba(14,165,233,0.10));
        color: var(--primary-strong);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .topbar h1 {
        margin-bottom: 8px;
        letter-spacing: -0.05em;
        font-size: clamp(2.2rem, 3vw, 3.3rem);
    }

    .topic-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.94) 0%, rgba(250,252,255,0.98) 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 18px 32px rgba(15, 23, 42, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .topic-card:hover {
        transform: translateY(-2px);
        border-color: rgba(67, 56, 202, 0.18);
        box-shadow: 0 22px 32px rgba(67, 56, 202, 0.07);
    }

    .pill {
        display: inline-block;
        background: var(--soft-primary);
        color: var(--primary);
        border-radius: 999px;
        padding: 6px 11px;
        font-size: 10px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .stButton > button {
        border-radius: 14px;
        font-weight: 800;
        padding: 0.7rem 1rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        box-shadow: 0 16px 26px rgba(67, 56, 202, 0.18);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #312e81 0%, #4338ca 100%);
    }

    .insight-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 10px 0 16px;
    }

    .insight-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(242,246,255,0.98) 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: 0 12px 20px rgba(15, 23, 42, 0.025);
    }

    .insight-box strong {
        display: inline-block;
        font-size: 1.4rem;
        margin-bottom: 4px;
    }

    .insight-box span {
        color: var(--muted);
        font-size: 0.82rem;
    }

    .compact-surface {
        padding-right: 0 !important;
        margin-right: 0 !important;
    }

    .topic-panel {
        background: linear-gradient(180deg, rgba(255,255,255,0.66) 0%, rgba(248,250,255,0.8) 100%);
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 24px;
        padding: 10px 12px 4px;
        margin-top: 4px;
        box-shadow: 0 12px 24px rgba(15,23,42,0.02);
    }

    .topic-list-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 10px 8px 8px;
    }

    .topic-list-header span {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="topbar">', unsafe_allow_html=True)
st.markdown("<div class='page-chip'>GD Spark</div>", unsafe_allow_html=True)
st.title("🎯 Choose Your GD Topic")
st.caption("Start with 5 fresh topics, then browse more until you find the perfect one.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="insight-strip">
        <div class="insight-box"><strong>5</strong><br><span>fresh ideas</span></div>
        <div class="insight-box"><strong>5+</strong><br><span>categories</span></div>
        <div class="insight-box"><strong>1</strong><br><span>best fit</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

main_area = st.columns([1.9, 0.9])
with main_area[0]:
    st.markdown('<div class="topic-panel">', unsafe_allow_html=True)
    st.markdown("<div class='topic-list-header'><span>Topics</span><span>Ready to explore</span></div>", unsafe_allow_html=True)
with main_area[1]:
    st.image(
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
        width=280,
        caption="Pick a topic that sparks conversation",
    )

with st.sidebar:
    st.header("Settings")
    st.selectbox("Category", ["All"] + sorted(topics.keys()), key="category")
    st.slider("Timer (minutes)", min_value=1, max_value=10, value=2, key="minutes")
    st.markdown("---")
    if st.session_state.history:
        st.subheader("Recent picks")
        for item in st.session_state.history:
            st.caption(f"• {item}")

if not st.session_state.pool:
    reset_topic_pool()

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("Generate fresh 5 topics", type="primary", use_container_width=True):
        reset_topic_pool()
with col_b:
    if st.button("Next 5 topics", use_container_width=True):
        next_batch()

for idx, (cat, topic) in enumerate(st.session_state.current_candidates):
    st.markdown('<div class="topic-card">', unsafe_allow_html=True)
    cols = st.columns([1, 6, 2, 2])
    with cols[0]:
        st.image(get_icon_path(cat), width=54)
    with cols[1]:
        st.markdown(f"<div class='pill'>{cat}</div>", unsafe_allow_html=True)
        st.markdown(f"**{topic}**")
    with cols[2]:
        if st.button("Select", key=f"select-{idx}-{topic}", use_container_width=True):
            select_candidate(cat, topic)
    with cols[3]:
        if st.button("Preview", key=f"preview-{idx}-{topic}", use_container_width=True):
            st.session_state.topic = topic
            st.session_state.topic_category = cat
            st.switch_page("pages/2_Prepare_GD.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Tip: Use the category filter to narrow down topics before you select one.")
