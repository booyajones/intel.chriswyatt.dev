import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Administrator\.openclaw\bigquery-key.json'
from google.cloud import bigquery
client = bigquery.Client(project='wyattplayground')

def q(sql):
    return list(client.query(sql).result())

P = 'wyattplayground'
D = 'dbt_prod_mart_power_bi_dataset'

# Check payment_metrics_full columns - this is what power bi uses for channel partner / customer
for tname in ['payment_metrics_full', 'payment_metrics', 'pbi_dim_supplier', 'dim_buyer', 'pbi_fact_order_denorm']:
    sql = f"""
    SELECT column_name, data_type 
    FROM `{P}.{D}.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = '{tname}'
    ORDER BY ordinal_position
    """
    try:
        cols = q(sql)
        print(f"\n=== {tname} ({len(cols)} cols) ===")
        for c in cols:
            print(f"  {c['column_name']}: {c['data_type']}")
    except Exception as e:
        print(f"\n=== {tname}: ERROR - {e}")
