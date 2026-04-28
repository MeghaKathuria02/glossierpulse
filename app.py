import json

import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import clean_customer_data, load_and_clean_data
from persona_generator import generate_brand_content, generate_persona_message
from segmentation import assign_segments, segment_summary


st.set_page_config(page_title="GlossierPulse", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

:root {
  --bg-main: #FAF7F2;
  --bg-sidebar: #F2EBE3;
  --sidebar-text: #3D2B1F;
  --text-main: #2C2C2C;
  --header-text: #3D2B1F;
  --accent: #B07D6E;
  --card-bg: #FFFFFF;
  --card-border: #E8DDD5;
  --muted-text: #7A6255;
}

.stApp {
  background: var(--bg-main);
  color: var(--text-main);
  font-family: "DM Sans", sans-serif;
}

.stMarkdown, .stText, p, span, label, div {
  color: var(--text-main);
}

.stSidebar, [data-testid="stSidebar"] {
  background: var(--bg-sidebar);
  border-right: 1px solid var(--card-border);
}

[data-testid="stSidebar"] * {
  color: var(--sidebar-text) !important;
}

.sidebar-circle {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: var(--accent);
  color: #FFFFFF !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin-bottom: 6px;
}

.sidebar-brand {
  color: var(--sidebar-text);
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.hero-title {
  color: var(--header-text);
  font-size: 2.6rem;
  font-weight: 700;
  text-align: center;
  margin-top: 8px;
  margin-bottom: 4px;
}

.hero-sub {
  color: var(--muted-text);
  text-align: center;
  margin-bottom: 12px;
}

.thin-divider {
  height: 1px;
  background: var(--card-border);
  margin: 10px 0 16px 0;
}

.page-title {
  color: var(--header-text);
  font-size: 1.9rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.page-subtitle {
  color: var(--muted-text);
  margin-bottom: 12px;
}

.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(61, 43, 31, 0.06);
  padding: 16px;
  margin-bottom: 12px;
}

.stat-card {
  background: #FFFFFF;
  border: 1px solid var(--card-border);
  border-top: 4px solid var(--accent);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(61, 43, 31, 0.05);
  padding: 14px;
}

.stat-label {
  color: var(--muted-text);
  font-size: 0.9rem;
}

.stat-value {
  color: var(--header-text);
  font-size: 1.55rem;
  font-weight: 700;
}

.feature-heading {
  color: var(--header-text);
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.feature-name {
  color: var(--header-text);
  font-weight: 700;
  margin-bottom: 4px;
}

.feature-desc {
  color: #6D645E;
  font-size: 0.92rem;
  min-height: 34px;
}

.about-box {
  background: #F5EEE8;
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 14px;
  color: var(--text-main);
}

.footer {
  text-align: center;
  color: #8A7B71;
  font-size: 0.82rem;
  margin-top: 18px;
}

.stButton > button {
  background: var(--accent) !important;
  color: #FFFFFF !important;
  border: 1px solid var(--accent) !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
}

.stSidebar .stButton > button {
  width: 100%;
  text-align: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
}

.stButton > button:hover {
  background: #9f7062 !important;
  border-color: #9f7062 !important;
  color: #FFFFFF !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div {
  background: #FFFFFF !important;
  color: #2C2C2C !important;
  border: 1px solid #E8DDD5 !important;
}

[data-testid="stFileUploader"] {
  background-color: #F2EBE3 !important;
  border: 1px solid #E8DDD5 !important;
  border-radius: 8px !important;
}

[data-testid="stFileUploader"] * {
  color: #2C2C2C !important;
}

[data-testid="stFileDropzoneInstructions"] {
  color: #7A6255 !important;
}

section[data-testid="stFileUploaderDropzone"] {
  background-color: #F2EBE3 !important;
  border: 1px dashed #B07D6E !important;
}

[data-testid="stFileUploaderDropzoneInput"] + div {
  background-color: #F2EBE3 !important;
  color: #2C2C2C !important;
}

[data-testid="stBaseButton-secondary"] {
  background-color: #FFFFFF !important;
  color: #2C2C2C !important;
  border: 1px solid #E8DDD5 !important;
}

.stFileUploader label {
  color: #2C2C2C !important;
}

button[data-testid="stBaseButton-secondary"] {
  background-color: #FFFFFF !important;
  color: #3D2B1F !important;
  border: 1px solid #B07D6E !important;
}

[data-testid="stSelectboxVirtualDropdown"] {
  background-color: #FFFFFF;
  color: #2C2C2C;
}

.stSelectbox [role="option"] {
  background-color: #FFFFFF;
  color: #2C2C2C;
}

.stSelectbox [role="option"]:hover {
  background-color: #F2EBE3;
  color: #2C2C2C;
}

.stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {
  color: #3D2B1F !important;
}

[data-testid="stMetricValue"] {
  color: #3D2B1F !important;
}

[data-testid="stDataFrame"] {
  border: 1px solid #E8DDD5;
  border-radius: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)


SIDEBAR_PAGES = ["Home", "Customer Segments", "AI Persona", "A/B Testing", "Trend Triggers"]
FEATURE_PAGES = ["Influencer Match Engine", "Collab Kit Builder", "Creator Outreach Generator"]
ALL_PAGES = SIDEBAR_PAGES + FEATURE_PAGES


def set_page(page_name: str) -> None:
    st.session_state["page"] = page_name


def render_footer() -> None:
    st.markdown('<div class="footer">GlossierPulse · 2026</div>', unsafe_allow_html=True)


def render_page_heading(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
            "age": [22, 28, 35, 41, 24, 30, 38, 45],
            "annual_income": [35000, 48000, 76000, 92000, 40000, 62000, 85000, 99000],
            "spending_score": [80, 65, 55, 35, 90, 70, 45, 30],
            "purchase_frequency": [12, 9, 7, 4, 14, 10, 5, 3],
        }
    )


if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if st.session_state["page"] not in ALL_PAGES:
    st.session_state["page"] = "Home"


# Sidebar UI
st.sidebar.markdown('<div class="sidebar-circle">GP</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-brand">GlossierPulse</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

for page in SIDEBAR_PAGES:
    if st.session_state["page"] == page:
        st.sidebar.markdown(
            f'<div style="background:#B07D6E;color:#FFFFFF;padding:8px 10px;border-radius:8px;margin-bottom:6px;font-weight:600;">{page}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.button(page, key=f"nav_{page}", use_container_width=True, on_click=set_page, args=(page,))

st.sidebar.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown("### Data")
uploaded_file = st.sidebar.file_uploader("Upload customer CSV", type=["csv"])
use_sample_data = st.sidebar.checkbox("Use sample data", value=True if uploaded_file is None else False)


# Shared data logic
try:
    if use_sample_data:
        raw_df = clean_customer_data(sample_dataframe())
    else:
        if uploaded_file is None:
            st.error("Please upload a CSV or enable sample data in the sidebar.")
            st.stop()
        raw_df = load_and_clean_data(uploaded_file)
except Exception as exc:
    st.error(f"Data loading error: {exc}")
    st.stop()

try:
    segmented_df = assign_segments(raw_df, n_clusters=4)
    summary_df = segment_summary(segmented_df)
except Exception as exc:
    st.error(f"Segmentation error: {exc}")
    st.stop()


current_page = st.session_state["page"]

if current_page == "Home":
    st.markdown('<div class="hero-title">GlossierPulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Know your customer. Speak their language.</div>', unsafe_allow_html=True)
    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

    total_customers = int(raw_df["customer_id"].nunique())
    segments_found = int(summary_df["segment_id"].nunique())
    avg_spending = round(float(raw_df["spending_score"].mean()), 1)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Total Customers</div><div class="stat-value">{total_customers}</div></div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Segments Found</div><div class="stat-value">{segments_found}</div></div>',
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Avg Spending Score</div><div class="stat-value">{avg_spending}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-heading">Marketing Tools</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            """
<div class="card">
  <div class="feature-name">-> Influencer Match Engine</div>
  <div class="feature-desc">Generate creator profile matches for your selected segment.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.button("Open Feature", key="open_influencer", use_container_width=True, on_click=set_page, args=("Influencer Match Engine",))
    with f2:
        st.markdown(
            """
<div class="card">
  <div class="feature-name">* Collab Kit Builder</div>
  <div class="feature-desc">Build a co-branded PR kit aligned to audience behavior.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.button("Open Feature", key="open_collab", use_container_width=True, on_click=set_page, args=("Collab Kit Builder",))
    with f3:
        st.markdown(
            """
<div class="card">
  <div class="feature-name">-> Creator Outreach Generator</div>
  <div class="feature-desc">Write outreach messages that stay warm, clear, and human.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.button("Open Feature", key="open_outreach", use_container_width=True, on_click=set_page, args=("Creator Outreach Generator",))

    st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="about-box">
GlossierPulse helps you understand customer segments, generate campaign personas, run A/B messaging simulations,
and create collaboration strategies that stay true to a human, skin-first brand voice.
</div>
""",
        unsafe_allow_html=True,
    )
    render_footer()

elif current_page == "Customer Segments":
    render_page_heading("Customer Segments", "Review segment patterns and performance signals.")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    scatter = px.scatter(
        segmented_df,
        x="annual_income",
        y="spending_score",
        color="segment_name",
        size="purchase_frequency",
        hover_data=["customer_id", "age"],
        title="Income vs Spending by Segment",
        template="plotly_white",
    )
    st.plotly_chart(scatter, use_container_width=True, key="segments_scatter")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(summary_df.round(2), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for idx, row in summary_df.reset_index(drop=True).iterrows():
        target = c1 if idx % 2 == 0 else c2
        with target:
            st.markdown(
                f"""
<div class="card">
<strong>{row["segment_name"]}</strong><br><br>
Customers: {int(row["customers"])}<br>
Avg Age: {row["avg_age"]:.1f}<br>
Avg Income: {row["avg_income"]:.1f}<br>
Avg Spending: {row["avg_spending"]:.1f}<br>
Avg Purchase Frequency: {row["avg_purchase_frequency"]:.1f}
</div>
""",
                unsafe_allow_html=True,
            )
    render_footer()

elif current_page == "AI Persona":
    render_page_heading("AI Persona", "Generate segment-specific persona messaging.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_segment = st.selectbox("Pick a segment", options=summary_df["segment_name"].tolist(), key="persona_segment")
        run_persona = st.button("Generate Persona Message", key="persona_button")
        st.markdown("</div>", unsafe_allow_html=True)
        if run_persona:
            try:
                segment_row = summary_df.loc[summary_df["segment_name"] == selected_segment].iloc[0]
                segment_stats = segment_row.to_dict()
                persona_text = generate_persona_message(segment_name=selected_segment, segment_stats=segment_stats)
                st.markdown(
                    f'<div class="card">{persona_text.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                st.error(f"Persona generation error: {exc}")
    render_footer()

elif current_page == "A/B Testing":
    render_page_heading("A/B Testing", "Compare scheduled and contextual campaign messages.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        selected_segment = st.selectbox("Pick a segment", options=summary_df["segment_name"].tolist(), key="ab_segment")
        st.markdown("</div>", unsafe_allow_html=True)

        segment_row = summary_df.loc[summary_df["segment_name"] == selected_segment].iloc[0]
        base_open_rate = float(26 + (segment_row["avg_spending"] * 0.08))
        base_click_rate = float(4.0 + (segment_row["avg_purchase_frequency"] * 0.18))
        base_conversion_rate = float(2.0 + (segment_row["avg_purchase_frequency"] * 0.1))
        version_a_metrics = {
            "open_rate": round(base_open_rate, 1),
            "click_rate": round(base_click_rate, 1),
            "conversion_rate": round(base_conversion_rate, 1),
        }
        version_b_metrics = {
            "open_rate": round(version_a_metrics["open_rate"] * 1.3, 1),
            "click_rate": round(version_a_metrics["click_rate"] * 1.3, 1),
            "conversion_rate": round(version_a_metrics["conversion_rate"] * 1.3, 1),
        }

        message_a = (
            f"Hey {selected_segment}, your evening skin reset is here. "
            "Our gentle routine is ready whenever your schedule opens up."
        )
        message_b = (
            f"Hey {selected_segment}, we noticed your skin might need a little extra support after a long day. "
            "Here is a simple, skin-first routine picked for this exact moment."
        )

        st.markdown(f'<div class="card"><strong>Version A</strong><br>{message_a}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><strong>Version B</strong><br>{message_b}</div>', unsafe_allow_html=True)

        metrics_df = pd.DataFrame(
            [
                {
                    "Version": "A - Standard Scheduled",
                    "Open Rate (%)": version_a_metrics["open_rate"],
                    "Click Rate (%)": version_a_metrics["click_rate"],
                    "Conversion Rate (%)": version_a_metrics["conversion_rate"],
                },
                {
                    "Version": "B - Trigger-Based Contextual",
                    "Open Rate (%)": version_b_metrics["open_rate"],
                    "Click Rate (%)": version_b_metrics["click_rate"],
                    "Conversion Rate (%)": version_b_metrics["conversion_rate"],
                },
            ]
        )
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        chart_df = metrics_df.melt(id_vars="Version", var_name="Metric", value_name="Rate")
        ab_chart = px.bar(
            chart_df,
            x="Metric",
            y="Rate",
            color="Version",
            barmode="group",
            title="Simulated A/B Performance",
            template="plotly_white",
        )
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(ab_chart, use_container_width=True, key="ab_metrics_chart")
        st.markdown("</div>", unsafe_allow_html=True)
    render_footer()

elif current_page == "Trend Triggers":
    render_page_heading("Trend Triggers", "Review contextual trigger windows by segment.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        trigger_segment = st.selectbox(
            "Select segment for trigger simulation",
            options=summary_df["segment_name"].tolist(),
            key="trigger_segment",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        row = summary_df.loc[summary_df["segment_name"] == trigger_segment].iloc[0]
        trigger_score = round(float((row["avg_spending"] * 0.5) + (row["avg_purchase_frequency"] * 4.2)), 1)
        suggested_window = "Evening (6 PM - 9 PM)" if row["avg_age"] < 35 else "Morning (7 AM - 10 AM)"
        st.markdown(
            f"""
<div class="card">
<strong>Context trigger score:</strong> {trigger_score}<br><br>
<strong>Best send window:</strong> {suggested_window}<br><br>
<strong>Suggested trigger:</strong> Deliver a skin-first reset message right after high-stress dayparts, then reinforce with short community proof.
</div>
""",
            unsafe_allow_html=True,
        )
    render_footer()

elif current_page == "Influencer Match Engine":
    st.button("Back to Home", key="back_home_influencer", on_click=set_page, args=("Home",))
    render_page_heading("Influencer Match Engine", "Generate creator profile matches for a segment.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        influencer_segment = st.selectbox(
            "Select segment for influencer matching",
            options=summary_df["segment_name"].tolist(),
            key="influencer_segment",
        )
        run_influencer = st.button("Generate Influencer Matches", key="influencer_button")
        st.markdown("</div>", unsafe_allow_html=True)
        if run_influencer:
            try:
                influencer_prompt = f"""
Create exactly 3 influencer profiles for this segment: {influencer_segment}.
Return ONLY valid JSON using this schema:
{{
  "profiles": [
    {{
      "profile_title": "short title",
      "example_creator_name": "fictional or representative creator name",
      "follower_range": "string",
      "content_style": "string",
      "platform": "string",
      "personality_type": "string",
      "why_fit": "2-3 lines on why this profile fits segment",
      "content_for_glossier": "2-3 lines on what content they should create"
    }}
  ]
}}
Use Glossier tone: honest, skin-first, community-first, never corporate.
"""
                influencer_raw = generate_brand_content(
                    user_prompt=influencer_prompt,
                    system_prompt="You are a creator strategy lead for Glossier. Output clean JSON only.",
                )
                influencer_data = json.loads(influencer_raw)
                profiles = influencer_data["profiles"]
                if len(profiles) != 3:
                    raise ValueError("Groq response did not return exactly 3 influencer profiles.")
                for idx, profile in enumerate(profiles, start=1):
                    st.markdown(
                        f"""
<div class="card">
<strong>Profile {idx}: {profile["profile_title"]}</strong><br><br>
Example creator: {profile["example_creator_name"]}<br>
Follower range: {profile["follower_range"]}<br>
Content style: {profile["content_style"]}<br>
Platform: {profile["platform"]}<br>
Personality type: {profile["personality_type"]}<br><br>
Why this fits: {profile["why_fit"]}<br><br>
Best content for Glossier: {profile["content_for_glossier"]}
</div>
""",
                        unsafe_allow_html=True,
                    )
            except Exception as exc:
                st.error(f"Influencer engine error: {exc}")
    render_footer()

elif current_page == "Collab Kit Builder":
    st.button("Back to Home", key="back_home_collab", on_click=set_page, args=("Home",))
    render_page_heading("Collab Kit Builder", "Build a co-branded kit around audience needs.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        collab_segment = st.selectbox(
            "Select segment for collab kit",
            options=summary_df["segment_name"].tolist(),
            key="collab_segment",
        )
        partner_type = st.selectbox(
            "Select collab partner type",
            options=[
                "Wellness Brand",
                "Fitness Brand",
                "Coffee Brand",
                "Mental Health Brand",
                "Fashion Brand",
                "Food & Drink Brand",
            ],
            key="partner_type",
        )
        run_collab = st.button("Generate Collab Kit", key="collab_button")
        st.markdown("</div>", unsafe_allow_html=True)
        if run_collab:
            try:
                collab_prompt = f"""
Build one full co-branded PR kit for:
- Segment: {collab_segment}
- Partner type: {partner_type}

Return ONLY valid JSON with this schema:
{{
  "kit_name": "string",
  "theme": "string",
  "glossier_products": ["product 1", "product 2", "product 3"],
  "partner_item_suggestion": "string",
  "handwritten_note_copy": "2-4 lines in Glossier voice",
  "campaign_hashtag": "string",
  "unboxing_experience": "2-4 lines describing the opening moment"
}}
Tone must be human, honest, skin-first, community-driven, never corporate.
"""
                collab_raw = generate_brand_content(
                    user_prompt=collab_prompt,
                    system_prompt="You are a Glossier brand partnerships strategist. Output clean JSON only.",
                )
                collab_data = json.loads(collab_raw)
                products_text = "<br>".join([f"- {item}" for item in collab_data["glossier_products"]])
                st.markdown(
                    f"""
<div class="card">
<strong>{collab_data["kit_name"]}</strong><br><br>
Theme: {collab_data["theme"]}<br><br>
Glossier products:<br>{products_text}<br><br>
Partner item suggestion: {collab_data["partner_item_suggestion"]}<br><br>
Handwritten note copy:<br>{collab_data["handwritten_note_copy"].replace(chr(10), "<br>")}<br><br>
Campaign hashtag: {collab_data["campaign_hashtag"]}<br><br>
Unboxing experience:<br>{collab_data["unboxing_experience"].replace(chr(10), "<br>")}
</div>
""",
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                st.error(f"Collab kit builder error: {exc}")
    render_footer()

elif current_page == "Creator Outreach Generator":
    st.button("Back to Home", key="back_home_outreach", on_click=set_page, args=("Home",))
    render_page_heading("Creator Outreach Generator", "Create outreach copy that is personal and clear.")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        creator_name = st.text_input("Creator name", key="creator_name")
        creator_niche = st.text_input("Content niche", key="creator_niche")
        creator_platform = st.text_input("Platform", key="creator_platform")
        outreach_segment = st.selectbox(
            "Select segment for outreach",
            options=summary_df["segment_name"].tolist(),
            key="outreach_segment",
        )
        run_outreach = st.button("Generate Outreach Copy", key="outreach_button")
        st.markdown("</div>", unsafe_allow_html=True)
        if run_outreach:
            try:
                outreach_prompt = f"""
Create outreach copy for this creator collaboration.
Creator name: {creator_name}
Content niche: {creator_niche}
Platform: {creator_platform}
Target segment: {outreach_segment}

Return ONLY valid JSON with this schema:
{{
  "dm_message": "under 150 words, casual and genuine",
  "email_subject": "string",
  "email_body": "formal but warm email",
  "follow_up_message": "follow-up after 1 week without reply"
}}
Voice: honest, human, skin-first, community-first, never corporate.
"""
                outreach_raw = generate_brand_content(
                    user_prompt=outreach_prompt,
                    system_prompt="You write creator outreach for Glossier. Output clean JSON only.",
                )
                outreach_data = json.loads(outreach_raw)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.text_area("Personalized DM", value=outreach_data["dm_message"], height=140)
                full_email = f"Subject: {outreach_data['email_subject']}\n\n{outreach_data['email_body']}"
                st.text_area("Formal Email", value=full_email, height=220)
                st.text_area("Follow-up Message", value=outreach_data["follow_up_message"], height=120)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as exc:
                st.error(f"Creator outreach error: {exc}")
    render_footer()
