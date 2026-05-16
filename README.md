# AI Search Visibility Tracker; Global Travel Brands

> How visible are the world's biggest travel brands when people ask AI instead of Google?

This project audits the AI search visibility of 15 global travel brands across 4 major AI engines; ChatGPT, Perplexity, Claude, and Gemini. It was built to answer the question that every major brand should be asking right now: *when a potential customer asks an AI assistant for a recommendation, do you show up?*

---

## Why I built this

AI search is reshaping how people discover brands. Tools like ChatGPT, Perplexity, and Gemini are becoming the new first stop for recommendations; replacing traditional search for millions of users. But unlike Google, there's no SEO playbook for AI visibility yet.

This project is an attempt to build one from scratch; starting with travel, one of the highest-intent consumer verticals.

---

## What I built

| Layer | Tool | Purpose |
|---|---|---|
| Data collection | Manual audit + structured prompt | 20 queries × 4 engines × 15 brands |
| Data warehouse | DuckDB | Local SQL-queryable database |
| Analysis | SQL | Insight extraction |
| Dashboard | Streamlit + Plotly | Interactive exploration |
| Agent | Python + Gemini API | Automated multi-engine data collection |

---

## The data

- **20 queries** across 7 intent categories: Transactional, Comparison, Trust/Safety, Use Case, Discovery, Planning, Intent/High Value
- **4 AI engines**: ChatGPT, Perplexity, Claude, Gemini
- **15 global travel brands**: Booking.com, Airbnb, Expedia, Skyscanner, TripAdvisor, Hostelworld, Kayak, Trivago, Hotels.com, Agoda, Vrbo, Google Flights, Omio, GetYourGuide, Hopper
- **221 brand mentions** recorded with position, sentiment, source citation, and response snippet

---

## Three notable findings

### 1. Booking.com and Google Flights dominate; but in completely different intent categories
Booking.com leads all mentions (39 total, first-recommended 23 times) and owns Trust/Safety and Use Case queries. Google Flights dominates Planning queries; appearing in 12 out of 12 planning mentions. This means AI visibility is intent-specific, not just volume-based. A brand optimising for one query type may be invisible in another.

### 2. Airbnb has a massive AI visibility gap
Despite being one of the world's most recognised travel brands, Airbnb appears only 15 times across all engines; and 6 of those are Trust/Safety queries (people asking "is Airbnb safe?"). It is virtually absent from Transactional and Planning queries, where Booking.com and Skyscanner dominate. For a brand this large, its AI search footprint is shockingly narrow.

### 3. ChatGPT cites sources far less than every other engine
ChatGPT cited sources only 62% of the time, compared to Gemini at 94%, Perplexity at 87%, and Claude at 84%. This has direct implications for brand strategy: Perplexity and Gemini's high citation rates mean SEO-rich brands with strong web presence have a structural advantage on those engines. Brands optimising only for ChatGPT are leaving 3 engines underserved.

---

## How to run it

**1. Clone the repo**
```bash
git clone https://github.com/nandnii/AI-Search-Visibility.git
cd AI-Search-Visibility
```

**2. Install dependencies**
```bash
pip install duckdb pandas openpyxl streamlit plotly
```

**3. Load data into DuckDB warehouse**
```bash
python load_data.py
```

**4. Launch the dashboard**
```bash
python3 -m streamlit run app.py
```

---

## Automated data collection agent

`ai_visibility_agent.py` is a multi-engine agent that automates data collection. It supports Gemini, ChatGPT, Perplexity, and Claude; activating only the engines for which API keys are set. Brand extraction uses Gemini as a structured output parser.

```bash
export GEMINI_API_KEY="your_key"
export OPENAI_API_KEY="your_key"      # optional
export ANTHROPIC_API_KEY="your_key"  # optional
export PERPLEXITY_API_KEY="your_key" # optional
python ai_visibility_agent.py
```

---

## What's next

- Expand to more verticals: Fashion, Pharma, Professional Services
- Track visibility changes over time (weekly snapshots)
- Build a scoring model: predict which brands are at risk of losing AI visibility
- Add a competitive benchmarking layer

---

## About

Built by Nandni Srivastava as a proof-of-work project exploring AI search visibility analytics; the analytical problem at the heart of what platforms like [Searchable](https://www.searchable.com) are solving for enterprise brands.
