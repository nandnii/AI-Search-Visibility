import pandas as pd
import duckdb

df = pd.read_excel("AI Search Visibility.xlsx", sheet_name="Raw Data", header=2)
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)
df = df[['query_id','query_text','query_category','engine',
         'brand_mentioned','position','sentiment',
         'source_cited','response_snippet']].copy()
df['position'] = pd.to_numeric(df['position'], errors='coerce')
df = df[df['brand_mentioned'].notna() & (df['brand_mentioned'] != 'none')]

con = duckdb.connect("visibility.duckdb")
con.execute("DROP TABLE IF EXISTS brand_mentions")
con.execute("CREATE TABLE brand_mentions AS SELECT * FROM df")
print(f"✅ Done! {len(df)} rows loaded into visibility.duckdb")
con.close()