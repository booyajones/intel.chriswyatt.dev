import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Administrator\.openclaw\bigquery-key.json'
from google.cloud import bigquery
client = bigquery.Client(project='wyattplayground')
P = 'wyattplayground'
D = 'dbt_prod_mart_power_bi_dataset'

# Check interchange / revenue / fee columns in payment_metrics_full
sql = f"""
SELECT column_name, data_type 
FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = 'payment_metrics_full' 
  AND (LOWER(column_name) LIKE '%interchange%' 
    OR LOWER(column_name) LIKE '%revenue%' 
    OR LOWER(column_name) LIKE '%fee%'
    OR LOWER(column_name) LIKE '%earn%')
ORDER BY column_name
"""
rows = list(client.query(sql).result())
print("=== Interchange/Revenue/Fee columns ===")
for r in rows:
    print(f"  {r['column_name']}: {r['data_type']}")

# Check card_interchange_report_full columns too
sql2 = f"""
SELECT column_name, data_type 
FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = 'card_interchange_report_full'
ORDER BY ordinal_position
"""
rows2 = list(client.query(sql2).result())
print("\n=== card_interchange_report_full columns ===")
for r in rows2:
    print(f"  {r['column_name']}: {r['data_type']}")
