import pandas as pd
import streamlit as st

st.set_page_config(page_title="Market Entry Risk and Opportunity Analyzer", layout="wide")

st.title("Market Entry Risk and Opportunity Analyzer")
st.caption("Consulting-style workflow for market-entry opportunity, risk and recommendation framing.")

with st.sidebar:
    st.header("Decision Settings")
    decision_stage = st.selectbox("Decision stage", ["Early screening", "Pre-investment diligence", "Leadership recommendation"])
    risk_appetite = st.selectbox("Risk appetite", ["Conservative", "Balanced", "Aggressive"])
    evidence_quality = st.slider("Evidence quality", 1, 5, 3)

company = st.text_input("Company or product", "Premium food export brand")
market = st.text_input("Target geography", "United Kingdom")
sector = st.text_input("Sector", "Packaged food / FMCG")
objective = st.text_area(
    "Client objective",
    height=80,
    value="Assess whether the company should enter the UK premium packaged-food market and identify the most important diligence questions before leadership review.",
)
notes = st.text_area(
    "Source notes",
    height=140,
    placeholder="Paste public report notes, regulator findings, competitor observations or customer insights.",
)

st.subheader("Issue Tree")
issue_tree = pd.DataFrame(
    {
        "Question": [
            "Is the market attractive?",
            "Can the company compete?",
            "Can the company operate compliantly?",
            "Is the unit economics case plausible?",
            "What evidence is missing?",
        ],
        "Analysis focus": [
            "Demand signals, customer segment, growth, price tolerance",
            "Competitor positioning, differentiation, route-to-market",
            "Licensing, labeling, customs, quality and documentation",
            "Margin, distribution cost, working capital, launch cost",
            "Market size, channel economics, regulatory timeline",
        ],
    }
)
st.dataframe(issue_tree, use_container_width=True, hide_index=True)

st.subheader("Assessment")
factors = [
    "Market demand",
    "Customer fit",
    "Competitive intensity",
    "Regulatory complexity",
    "Operational readiness",
    "Margin potential",
    "Evidence confidence",
]
scores = {}
cols = st.columns(2)
for index, factor in enumerate(factors):
    with cols[index % 2]:
        default = evidence_quality if factor == "Evidence confidence" else 3
        scores[factor] = st.slider(factor, 1, 5, default)

scorecard = pd.DataFrame({"Factor": list(scores.keys()), "Score": list(scores.values())})
st.dataframe(scorecard, use_container_width=True, hide_index=True)

opportunity_score = round((scores["Market demand"] + scores["Customer fit"] + scores["Margin potential"]) / 3, 1)
risk_score = round((scores["Competitive intensity"] + scores["Regulatory complexity"] + (6 - scores["Operational readiness"])) / 3, 1)
confidence_score = scores["Evidence confidence"]

threshold = {"Conservative": 0.8, "Balanced": 0.3, "Aggressive": -0.2}[risk_appetite]
net_signal = round(opportunity_score - risk_score + ((confidence_score - 3) * 0.2), 1)

if confidence_score <= 2:
    stance = "Investigate before decision"
elif net_signal >= threshold:
    stance = "Proceed to business case"
elif net_signal >= -0.5:
    stance = "Investigate before decision"
else:
    stance = "Hold / do not enter yet"

col1, col2, col3 = st.columns(3)
col1.metric("Opportunity score", opportunity_score)
col2.metric("Risk score", risk_score)
col3.metric("Recommended stance", stance)

st.subheader("Risk Heatmap")
risk_rows = pd.DataFrame(
    {
        "Risk area": ["Regulatory", "Competitive", "Operational", "Financial", "Evidence"],
        "Current signal": [
            "High" if scores["Regulatory complexity"] >= 4 else "Medium" if scores["Regulatory complexity"] == 3 else "Low",
            "High" if scores["Competitive intensity"] >= 4 else "Medium" if scores["Competitive intensity"] == 3 else "Low",
            "High" if scores["Operational readiness"] <= 2 else "Medium" if scores["Operational readiness"] == 3 else "Low",
            "High" if scores["Margin potential"] <= 2 else "Medium" if scores["Margin potential"] == 3 else "Low",
            "High" if confidence_score <= 2 else "Medium" if confidence_score == 3 else "Low",
        ],
        "Diligence question": [
            "What licenses, labeling rules, customs requirements and quality controls apply?",
            "Which competitors own the premium segment, and how defensible is differentiation?",
            "Can sourcing, logistics, documentation and service levels support launch?",
            "Do price, channel margins and launch costs produce a credible return?",
            "Which claims are sourced, current and decision-grade?",
        ],
    }
)
st.dataframe(risk_rows, use_container_width=True, hide_index=True)

st.subheader("Draft Recommendation")
st.write(
    f"For {company} entering {market} in {sector}, the current signal is **{stance}**. "
    f"The opportunity score is {opportunity_score}/5, risk score is {risk_score}/5 and evidence confidence is {confidence_score}/5. "
    "The recommendation should remain conditional until the highest-risk assumptions are validated with current sources."
)

st.subheader("Next Diligence Checklist")
st.markdown(
    "- Validate market size and customer segment\n"
    "- Identify top five competitors and price points\n"
    "- Confirm licensing, customs, labeling and compliance requirements\n"
    "- Map distribution partners and operating costs\n"
    "- Build base, upside and downside scenarios"
)

memo = f"""# Market Entry Risk and Opportunity Memo

## Company / Product
{company}

## Target Market
{market}

## Sector
{sector}

## Objective
{objective}

## Decision Stage
{decision_stage}

## Recommendation
{stance}

## Scores
- Opportunity score: {opportunity_score}/5
- Risk score: {risk_score}/5
- Evidence confidence: {confidence_score}/5
- Net signal: {net_signal}

## Source Notes
{notes or "No source notes provided. Treat findings as assumption-led until evidence is added."}

## Key Risks
{chr(10).join("- " + row["Risk area"] + ": " + row["Diligence question"] for _, row in risk_rows.iterrows())}

## Next Diligence Checklist
- Validate market size and customer segment
- Identify top five competitors and price points
- Confirm licensing, customs, labeling and compliance requirements
- Map distribution partners and operating costs
- Build base, upside and downside scenarios
"""

st.download_button(
    "Download Market Entry Memo",
    data=memo,
    file_name="market_entry_risk_opportunity_memo.md",
    mime="text/markdown",
)
