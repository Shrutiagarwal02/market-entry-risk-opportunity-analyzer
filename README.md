# Market Entry Risk and Opportunity Analyzer

Consulting analyst workflow for assessing whether a company should enter a new geography, sector or product market.

## Recruiter Signal

This project shows business consulting judgment: problem structuring, issue trees, market-entry analysis, risk assessment, recommendation writing and assumption discipline.

It is designed for roles such as:

- Consulting Analyst
- Strategy Analyst
- Business Analyst
- Market Research Analyst
- Growth / Expansion Analyst

## Inputs

- Target company or product
- Target geography
- Sector
- Known constraints
- Source notes from public reports, regulator pages, news or company disclosures
- Assumptions and missing evidence

## Outputs

- Opportunity summary
- Competitor and customer scan
- Regulatory and operational risk heatmap
- Key assumptions
- Go / no-go / investigate recommendation
- Next-step diligence checklist
- Exportable market-entry memo

## Why This Matters

Consulting and strategy roles require more than a generic recommendation. A strong analyst must define the market-entry question, structure the issue tree, score opportunity and risk, identify missing evidence and convert findings into a practical next-step plan.

## Tech Stack

- Streamlit
- pandas

## How To Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

- CSV upload for competitor data
- Source-link tracking for public evidence
- Scenario model for base, upside and downside cases
- Export to DOCX/PDF
- AI-assisted first draft based only on user-provided source notes

## Responsible AI Boundary

The app should not invent market data. It should require source notes or clearly label assumptions when data is missing.

