import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Search Visibility — Travel Brands",
    page_icon="🔍",
    layout="wide"
)

# ── Connect to DuckDB ──────────────────────────────────────────────────────────
@st.cache_resource
def get_con():
    return duckdb.connect("visibility.duckdb", read_only=True)

con = get_con()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")
all_engines = con.execute("SELECT DISTINCT engine FROM brand_mentions ORDER BY engine").df()['engine'].tolist()
all_categories = con.execute("SELECT DISTINCT query_category FROM brand_mentions ORDER BY query_category").df()['query_category'].tolist()

selected_engines = st.sidebar.multiselect("Engines", all_engines, default=all_engines)
selected_categories = st.sidebar.multiselect("Query categories", all_categories, default=all_categories)

engine_filter = "', '".join(selected_engines)
category_filter = "', '".join(selected_categories)

def q(sql):
    return con.execute(sql).df()

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("AI Search Visibility Tracker")
st.caption("Global travel brands · 4 AI engines · 20 queries · Built for Searchable")
st.divider()

# ── Metric cards ───────────────────────────────────────────────────────────────
total = q(f"SELECT COUNT(*) as n FROM brand_mentions WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')").iloc[0]['n']
unique_brands = q(f"SELECT COUNT(DISTINCT brand_mentioned) as n FROM brand_mentions WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')").iloc[0]['n']
top_brand = q(f"SELECT brand_mentioned FROM brand_mentions WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}') GROUP BY brand_mentioned ORDER BY COUNT(*) DESC LIMIT 1").iloc[0]['brand_mentioned']
pct_cited = q(f"SELECT ROUND(100.0 * COUNT(CASE WHEN source_cited='Yes' THEN 1 END) / COUNT(*), 1) as pct FROM brand_mentions WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')").iloc[0]['pct']

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total brand mentions", total)
col2.metric("Unique brands mentioned", unique_brands)
col3.metric("Most visible brand", top_brand)
col4.metric("Avg citation rate", f"{pct_cited}%")

st.divider()

# ── Row 1: Brand mentions + Position 1 ────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Brand mention count")
    df_mentions = q(f"""
        SELECT brand_mentioned, COUNT(*) as mentions
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY brand_mentioned
        ORDER BY mentions DESC
    """)
    fig = px.bar(df_mentions, x='brand_mentioned', y='mentions',
                 color='mentions', color_continuous_scale='Blues',
                 labels={'brand_mentioned': '', 'mentions': 'Mentions'})
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      margin=dict(t=10, b=10), height=320)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Times recommended first (position 1)")
    df_pos1 = q(f"""
        SELECT brand_mentioned, COUNT(*) as times_first
        FROM brand_mentions
        WHERE position = 1
        AND engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY brand_mentioned
        ORDER BY times_first DESC
    """)
    fig2 = px.bar(df_pos1, x='brand_mentioned', y='times_first',
                  color='times_first', color_continuous_scale='Greens',
                  labels={'brand_mentioned': '', 'times_first': 'Times first'})
    fig2.update_layout(showlegend=False, coloraxis_showscale=False,
                       margin=dict(t=10, b=10), height=320)
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Heatmap — brand × category ─────────────────────────────────────────
st.subheader("Brand visibility by query category")
df_heat = q(f"""
    SELECT query_category, brand_mentioned, COUNT(*) as mentions
    FROM brand_mentions
    WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
    GROUP BY query_category, brand_mentioned
""")
heat_pivot = df_heat.pivot_table(index='query_category', columns='brand_mentioned',
                                  values='mentions', fill_value=0)
fig3 = px.imshow(heat_pivot, color_continuous_scale='Blues',
                 labels=dict(x='Brand', y='Query category', color='Mentions'),
                 aspect='auto')
fig3.update_layout(margin=dict(t=10, b=10), height=300)
st.plotly_chart(fig3, use_container_width=True)

# ── Row 3: Engine comparison + Citation rate ───────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Mentions per engine")
    df_eng = q(f"""
        SELECT engine, brand_mentioned, COUNT(*) as mentions
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY engine, brand_mentioned
        ORDER BY mentions DESC
    """)
    fig4 = px.bar(df_eng, x='engine', y='mentions', color='brand_mentioned',
                  labels={'engine': '', 'mentions': 'Mentions', 'brand_mentioned': 'Brand'})
    fig4.update_layout(margin=dict(t=10, b=10), height=320)
    st.plotly_chart(fig4, use_container_width=True)

with col_d:
    st.subheader("Citation rate by engine")
    df_cite = q(f"""
        SELECT engine,
               ROUND(100.0 * COUNT(CASE WHEN source_cited='Yes' THEN 1 END) / COUNT(*), 1) as pct_cited
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY engine
        ORDER BY pct_cited DESC
    """)
    fig5 = px.bar(df_cite, x='engine', y='pct_cited',
                  color='pct_cited', color_continuous_scale='Oranges',
                  labels={'engine': '', 'pct_cited': 'Citation rate (%)'},
                  text='pct_cited')
    fig5.update_traces(texttemplate='%{text}%', textposition='outside')
    fig5.update_layout(showlegend=False, coloraxis_showscale=False,
                       margin=dict(t=30, b=10), height=320, yaxis_range=[0, 110])
    st.plotly_chart(fig5, use_container_width=True)

# ── Row 4: Average position + Sentiment ───────────────────────────────────────
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Average position per brand")
    st.caption("Lower = mentioned earlier = better visibility")
    df_avgpos = q(f"""
        SELECT brand_mentioned, ROUND(AVG(position), 2) as avg_position
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY brand_mentioned
        ORDER BY avg_position ASC
    """)
    fig6 = px.bar(df_avgpos, x='brand_mentioned', y='avg_position',
                  color='avg_position', color_continuous_scale='RdYlGn_r',
                  labels={'brand_mentioned': '', 'avg_position': 'Avg position'})
    fig6.update_layout(showlegend=False, coloraxis_showscale=False,
                       margin=dict(t=10, b=10), height=320)
    fig6.update_xaxes(tickangle=45)
    st.plotly_chart(fig6, use_container_width=True)

with col_f:
    st.subheader("Sentiment breakdown")
    df_sent = q(f"""
        SELECT brand_mentioned, sentiment, COUNT(*) as n
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        GROUP BY brand_mentioned, sentiment
        ORDER BY brand_mentioned
    """)
    fig7 = px.bar(df_sent, x='brand_mentioned', y='n', color='sentiment',
                  color_discrete_map={'Positive': '#22c55e', 'Neutral': '#f59e0b', 'Negative': '#ef4444'},
                  labels={'brand_mentioned': '', 'n': 'Count', 'sentiment': 'Sentiment'})
    fig7.update_layout(margin=dict(t=10, b=10), height=320)
    fig7.update_xaxes(tickangle=45)
    st.plotly_chart(fig7, use_container_width=True)

# ── Raw data table ─────────────────────────────────────────────────────────────
st.divider()
with st.expander("View raw data"):
    df_raw = q(f"""
        SELECT query_id, query_text, query_category, engine,
               brand_mentioned, position, sentiment, source_cited, response_snippet
        FROM brand_mentions
        WHERE engine IN ('{engine_filter}') AND query_category IN ('{category_filter}')
        ORDER BY query_id, engine, position
    """)
    st.dataframe(df_raw, use_container_width=True)

st.caption("Data collected across ChatGPT, Perplexity, Claude & Gemini · Proof-of-work project for Searchable application")