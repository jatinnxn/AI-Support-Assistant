import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Support AI Assistant",
    page_icon="🤖",
    layout="wide",
)

st.markdown("""
<style>

.main{
    padding-top:1rem;
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:#f8f9fa;
    padding:15px;
    border-radius:10px;
    border:1px solid #dcdcdc;
}

.success-card{
    background:#e8f5e9;
    padding:15px;
    border-radius:10px;
}

.warning-card{
    background:#fff3cd;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Support Assistant")

st.write(
    "Production-grade AI Support Assistant powered by Gemini + RAG"
)

tab1, tab2 = st.tabs(
    [
        "🎫 Ticket Triage",
        "📊 TAM Summary",
    ]
)

###########################################################
# TAB 1
###########################################################

with tab1:

    st.header("Ticket Triage")

    subject = st.text_input(
        "Subject"
    )

    body = st.text_area(
        "Body",
        height=180,
    )

    if st.button(
        "Analyze Ticket",
        use_container_width=True,
    ):

        if not subject or not body:

            st.error(
                "Subject and Body are required."
            )

        else:

            with st.spinner(
                "Analyzing ticket..."
            ):

                response = requests.post(
                    f"{API_URL}/triage",
                    json={
                        "subject": subject,
                        "body": body,
                    },
                )

            if response.status_code == 200:

                result = response.json()

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Product Area",
                        result["product_area"],
                    )

                with c2:
                    st.metric(
                        "Category",
                        result["issue_category"],
                    )

                with c3:
                    st.metric(
                        "Urgency",
                        result["urgency"],
                    )

                st.divider()

                st.subheader("Reasoning")

                st.info(
                    result["reasoning"]
                )

                st.subheader(
                    "Knowledge Base"
                )

                st.success(
                    result["knowledge_base_article"]
                )

                st.subheader(
                    "Responder Team"
                )

                st.warning(
                    result["responder_team"]
                )

                st.subheader(
                    "Suggested First Response"
                )

                st.text_area(
                    "",
                    value=result["first_response"],
                    height=220,
                )

            else:

                st.error(
                    response.text
                )

###########################################################
# TAB 2
###########################################################

with tab2:

    st.header("Technical Account Manager")

    account_id = st.text_input(
        "Account ID",
        value="ACC-3336",
        key="account_id",
    )

    if st.button(
        "Generate Account Summary",
        use_container_width=True,
    ):

        if not account_id.strip():

            st.error("Account ID is required.")

        else:

            with st.spinner("Generating executive summary..."):

                response = requests.get(
                    f"{API_URL}/tam/{account_id}"
                )

            if response.status_code == 200:

                result = response.json()

                st.success("Summary generated successfully.")

                st.subheader("Executive Summary")

                st.info(
                    result["executive_summary"]
                )

                st.divider()

                st.subheader("Open Risks")

                risk_rows = []

                for risk in result["open_risks"]:

                    risk_rows.append(
                        {
                            "Risk": risk["risk"],
                            "Evidence": risk["evidence"],
                        }
                    )

                if risk_rows:

                    df = pd.DataFrame(risk_rows)

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                    )

                st.divider()

                st.subheader("Talking Points")

                for point in result["talking_points"]:

                    st.markdown(f"- {point}")

            elif response.status_code == 404:

                st.error(
                    response.json()["detail"]
                )

            else:

                st.error(
                    "Failed to generate account summary."
                )

###########################################################
# FOOTER
###########################################################

st.divider()

try:

    health = requests.get(
        f"{API_URL}/",
        timeout=2,
    )

    if health.status_code == 200:

        st.success(
            "✅ FastAPI backend connected."
        )

    else:

        st.warning(
            "⚠ Backend is running but returned an unexpected status."
        )

except requests.exceptions.ConnectionError:

    st.error(
        "❌ FastAPI backend is not running.\n\n"
        "Start it using:\n\n"
        "uvicorn app.main:app --reload"
    )

except Exception as e:

    st.error(str(e))