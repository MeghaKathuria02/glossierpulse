import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import clean_customer_data, load_and_clean_data
from persona_generator import generate_persona_message
from segmentation import assign_segments, segment_summary


st.set_page_config(page_title="GlossierPulse", page_icon="💄", layout="wide")

st.title("GlossierPulse")
st.caption("Segment beauty customers and generate AI campaign personas in Glossier voice.")


def _render_upload_help() -> None:
    st.info(
        "Upload a CSV with columns: "
        "`customer_id, age, annual_income, spending_score, purchase_frequency`"
    )


def _sample_dataframe() -> pd.DataFrame:
    # Small starter dataset so beginners can test quickly.
    return pd.DataFrame(
        {
            "customer_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
            "age": [22, 28, 35, 41, 24, 30, 38, 45],
            "annual_income": [35000, 48000, 76000, 92000, 40000, 62000, 85000, 99000],
            "spending_score": [80, 65, 55, 35, 90, 70, 45, 30],
            "purchase_frequency": [12, 9, 7, 4, 14, 10, 5, 3],
        }
    )


uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])

left_col, right_col = st.columns([1, 1])
with left_col:
    use_sample_data = st.checkbox("Use sample data instead", value=True if uploaded_file is None else False)

if uploaded_file is None and not use_sample_data:
    _render_upload_help()
    st.stop()

try:
    if use_sample_data:
        raw_df = clean_customer_data(_sample_dataframe())
    else:
        raw_df = load_and_clean_data(uploaded_file)

except Exception as exc:
    st.error(f"Data loading error: {exc}")
    st.stop()

st.subheader("Customer Data Preview")
st.dataframe(raw_df, use_container_width=True)

try:
    segmented_df = assign_segments(raw_df, n_clusters=4)
    summary_df = segment_summary(segmented_df)
except Exception as exc:
    st.error(f"Segmentation error: {exc}")
    st.stop()

st.subheader("Segment Distribution")
chart = px.scatter(
    segmented_df,
    x="annual_income",
    y="spending_score",
    color="segment_name",
    size="purchase_frequency",
    hover_data=["customer_id", "age"],
    title="Income vs Spending by Segment",
)
st.plotly_chart(chart, use_container_width=True)

st.subheader("Segment Summary")
st.dataframe(summary_df.round(2), use_container_width=True)

st.subheader("AI Persona Generator")
selected_segment = st.selectbox("Pick a segment", options=summary_df["segment_name"].tolist())
generate_clicked = st.button("Generate Persona Message")

if generate_clicked:
    try:
        segment_row = summary_df.loc[summary_df["segment_name"] == selected_segment].iloc[0]
        segment_stats = segment_row.to_dict()
        persona_text = generate_persona_message(
            segment_name=selected_segment,
            segment_stats=segment_stats,
        )
        st.success("Persona generated successfully.")
        st.markdown(persona_text)
    except Exception as exc:
        st.error(f"Persona generation error: {exc}")

st.subheader("A/B Testing Simulation")
st.caption(
    "Compare two campaign styles for the selected segment in Glossier voice. "
    "Version B is modeled to perform about 30% better."
)

# Get the selected segment stats and build deterministic metrics.
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

copy_col_a, copy_col_b = st.columns(2)
with copy_col_a:
    st.markdown("**Version A - Standard Scheduled Message**")
    st.info(message_a)
with copy_col_b:
    st.markdown("**Version B - Trigger-Based Contextual Message**")
    st.info(message_b)

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

st.dataframe(metrics_df, use_container_width=True, hide_index=True)

chart_df = metrics_df.melt(id_vars="Version", var_name="Metric", value_name="Rate")
metrics_chart = px.bar(
    chart_df,
    x="Metric",
    y="Rate",
    color="Version",
    barmode="group",
    title="Simulated A/B Performance",
)
st.plotly_chart(metrics_chart, use_container_width=True)

st.success(
    "Winner: Version B. Contextual timing plus human, skin-first messaging drives roughly 30% higher results."
)
