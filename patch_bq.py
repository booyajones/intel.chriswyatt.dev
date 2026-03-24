import os
import re

with open("fetch_bq_data.py", "r", encoding="utf-8") as f:
    code = f.read()

# Add the propensity query to CUSTOMER_VALUE_QUERIES
propensity_query = """
    "supplierPropensity": f\"\"\"
SELECT
    s.db_supplier_name AS supplier_name,
    COUNT(p.payment_id) AS frequency,
    AVG(p.payment_amount) AS avg_size,
    SUM(p.payment_amount) AS total_volume,
    MAX(s.combined_payment_method) AS method
FROM {tbl('pbi_dim_supplier')} s
JOIN {tbl('pbi_star_payment_fact')} p
  ON s.db_supplier_uuid = p.payment_supplier_id
WHERE LOWER(s.combined_payment_method) IN ('check', 'ach')
GROUP BY s.db_supplier_name
HAVING total_volume > 1000 AND frequency > 1
ORDER BY total_volume DESC
LIMIT 500
\"\"\",
"""

code = code.replace('"supplierMethodBreakdown": f"""', propensity_query + '\n    "supplierMethodBreakdown": f"""')

# Add to the data returned in build_customer_value
propensity_parse = """
    print("  Querying supplier propensity...")
    propensity_rows = run_query(client, CUSTOMER_VALUE_QUERIES["supplierPropensity"], dry_run) or []
    supplier_propensity = [
        {
            "supplier_name": r.get("supplier_name"),
            "frequency": int(r.get("frequency") or 0),
            "avg_size": float(r.get("avg_size") or 0),
            "total_volume": float(r.get("total_volume") or 0),
            "method": r.get("method")
        }
        for r in propensity_rows
    ]
"""

code = code.replace('return {\n        "kpis":', propensity_parse + '\n    return {\n        "supplierPropensity": supplier_propensity,\n        "kpis":')

# Write back
with open("fetch_bq_data.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Patched fetch_bq_data.py")