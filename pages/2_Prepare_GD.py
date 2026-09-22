import math
import time

import streamlit as st

st.set_page_config(page_title="GD Preparation", page_icon="📝", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f3f7ff;
        --panel: rgba(255,255,255,0.9);
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
            radial-gradient(circle at top left, rgba(67, 56, 202, 0.18), transparent 28%),
            radial-gradient(circle at bottom right, rgba(14, 165, 233, 0.14), transparent 28%),
            linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.4rem;
        max-width: 1360px;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.45rem;
    }

    .prep-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(242,247,255,0.96) 100%);
        border: 1px solid var(--border);
        border-radius: 30px;
        padding: 22px 22px 18px;
        box-shadow: var(--shadow);
        margin-bottom: 12px;
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

    .highlight {
        display: inline-block;
        background: var(--soft-primary);
        color: var(--primary);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 14px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .compact-image {
        max-width: 220px !important;
        border-radius: 22px;
        box-shadow: 0 18px 28px rgba(15, 23, 42, 0.12);
        margin-right: 12px;
    }

    .topic-heading {
        margin-top: 0;
        margin-bottom: 8px;
        letter-spacing: -0.04em;
        font-size: clamp(2rem, 3vw, 2.7rem);
    }

    .stButton > button {
        border-radius: 14px;
        font-weight: 800;
        padding: 0.7rem 1rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        box-shadow: 0 14px 22px rgba(67, 56, 202, 0.16);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "topic" not in st.session_state or not st.session_state.topic:
    st.warning("No topic selected yet. Go back and choose one from the topic page.")
    if st.button("Go to topic page"):
        st.switch_page("pages/1_Choose_Topic.py")
    st.stop()


TOPIC_IMAGES = {
    "Should voting be made compulsory in India?": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=900&q=80",
    "Is the gig economy a boon or a bane for young workers?": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
    "One Nation, One Election: practical or problematic?": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
    "Are freebies during elections good for democracy?": "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=900&q=80",
    "Should there be a cap on the number of terms a politician can serve?": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=900&q=80",
    "Is India ready for a cashless economy?": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=900&q=80",
    "Will AI replace more jobs than it creates?": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "Social media: connecting people or isolating them?": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=900&q=80",
    "Should there be strict regulations on AI-generated content?": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=80",
    "Is work from home here to stay?": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
    "Are electric vehicles truly the future of transport?": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=900&q=80",
    "Data privacy vs. national security": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
    "Is the education system producing degrees but not skills?": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
    "Should schools teach financial literacy as a compulsory subject?": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=900&q=80",
    "Brain drain: a loss or a gain for developing countries?": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=900&q=80",
    "Is cancel culture justified?": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
    "Should there be a uniform civil code?": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&w=900&q=80",
    "Mental health awareness: are we doing enough?": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=900&q=80",
    "Startups vs. stable jobs: which is better for freshers?": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
    "Is the rise of e-commerce killing small local businesses?": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=900&q=80",
    "Should India focus on manufacturing or services for growth?": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=900&q=80",
    "Are unpaid internships exploitation?": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=900&q=80",
    "Cryptocurrency: innovation or speculation?": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&w=900&q=80",
    "Is a 4-day work week practical?": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
    "Blue is better than red": "https://images.unsplash.com/photo-1515405295579-ba7b45403062?auto=format&fit=crop&w=900&q=80",
    "Is failure the best teacher?": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
    "The pen is mightier than the sword": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=900&q=80",
    "Is silence golden?": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
    "Zero: a hero or a villain?": "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&w=900&q=80",
    "Should we live to work or work to live?": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=900&q=80",
}

CATEGORY_IMAGES = {
    "Current Affairs": "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=900&q=80",
    "Technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "Social Issues": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=900&q=80",
    "Business & Economy": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=900&q=80",
    "Abstract": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
}


def generate_details(topic: str, category: str):
    base = topic.rstrip("?\n ")
    lower = base.lower()

    if lower.startswith("should"):
        subject = base[7:].strip()
        summary = f"This topic asks whether {subject.lower()} should be supported, restricted, or reformed in a practical and ethical way."
        for_points = [
            f"Positive impact on society if {subject.lower()} is adopted thoughtfully.",
            "Improves fairness, accessibility, or efficiency for a wider group.",
            "Creates a strong case for reform backed by evidence and public welfare.",
        ]
        against_points = [
            f"Implementation may be difficult or expensive for {subject.lower()}.",
            "Could lead to unintended consequences or public resistance.",
            "Requires careful policy design and strong accountability.",
        ]
    elif lower.startswith(("is", "are", "will", "can")):
        summary = f"This topic explores whether {lower} is realistic, beneficial, and sustainable in the present context."
        for_points = [
            "Strong practical benefits or social advantage.",
            "Clear examples showing long-term improvement.",
            "A convincing case can be built using data and current trends.",
        ]
        against_points = [
            "There are significant limitations or counterexamples.",
            "Short-term costs may outweigh long-term gain.",
            "Ethical, political, or social trade-offs remain unresolved.",
        ]
    else:
        summary = f"This question invites discussion on the meaning, impact, and relevance of {base.lower()} in modern life and public decision-making."
        for_points = [
            "It connects to everyday life and public values.",
            "It allows thoughtful examples, stories, and debates.",
            "It encourages balanced reasoning instead of emotional reactions.",
        ]
        against_points = [
            "It may be interpreted too broadly or vaguely.",
            "Arguments can sound abstract without examples.",
            "It may need strong framing to stay focused and relevant.",
        ]

    return {
        "summary": summary,
        "for_points": for_points,
        "against_points": against_points,
        "opening": "This topic matters because it affects real people, institutions, and public choices. The core debate is not whether the issue exists, but how we should respond to it in a fair and practical way.",
        "closing": "The best answer is not extreme. A balanced view that weighs benefits, risks, and real-world impact is usually the strongest argument in a GD.",
        "structure": [
            "Introduction: define the topic and explain why it matters.",
            "Point 1: state your strongest supporting argument.",
            "Point 2: address the main opposing view with fairness.",
            "Conclusion: give a clear, balanced final stand.",
        ],
        "tips": [
            "Use 2-3 concrete examples instead of listing too many random points.",
            "Stay calm, balanced, and confident rather than aggressive.",
            "End with a memorable takeaway that shows judgment and clarity.",
        ],
        "category": category,
    }


details = generate_details(st.session_state.topic, st.session_state.topic_category)

st.markdown("<div class='page-chip'>GD Spark</div>", unsafe_allow_html=True)
header_col, text_col = st.columns([0.8, 2.2])
with header_col:
    image_url = TOPIC_IMAGES.get(st.session_state.topic, CATEGORY_IMAGES.get(st.session_state.topic_category, CATEGORY_IMAGES["Abstract"]))
    st.image(
        image_url,
        width=220,
        output_format="auto",
        clamp=True,
    )
with text_col:
    st.markdown(f"<div class='highlight'>{st.session_state.topic_category}</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='topic-heading'>{st.session_state.topic}</h2>", unsafe_allow_html=True)
    st.write("A focused GD topic with arguments, examples, and a balanced speaking approach.")

st.markdown('<div class="prep-box">', unsafe_allow_html=True)
content_col, side_col = st.columns([1.4, 1])

with content_col:
    st.subheader("Topic summary")
    st.write(details["summary"])

    st.subheader("GD structure")
    for item in details["structure"]:
        st.write(f"• {item}")

    st.subheader("Opening line")
    st.write(details["opening"])

    st.subheader("Closing line")
    st.write(details["closing"])

    st.subheader("Speaking tips")
    for tip in details["tips"]:
        st.write(f"• {tip}")

with side_col:
    col_for, col_against = st.columns(2)
    with col_for:
        st.subheader("For")
        for point in details["for_points"]:
            st.write(f"• {point}")
    with col_against:
        st.subheader("Against")
        for point in details["against_points"]:
            st.write(f"• {point}")

    st.markdown("---")
    st.subheader("Timer")
    st.slider("Minutes", min_value=1, max_value=10, value=st.session_state.get("minutes", 2), key="minutes")
    if st.button("Start timer", type="primary", use_container_width=True):
        st.session_state.end_time = time.time() + st.session_state.minutes * 60
        st.session_state.total = st.session_state.minutes * 60
        st.session_state.alerted = False

    if st.session_state.get("end_time"):
        remaining = math.ceil(st.session_state.end_time - time.time())
        if remaining > 0:
            minutes, seconds = divmod(remaining, 60)
            st.markdown(f"## ⏱️ {minutes:02d}:{seconds:02d}")
            st.progress(min(remaining / max(st.session_state.total, 1), 1.0))
        else:
            st.markdown("## ⏰ Time’s up!")
            st.balloons()
            st.session_state.alerted = True

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
if st.button("Back to topic selection"):
    st.switch_page("pages/1_Choose_Topic.py")
