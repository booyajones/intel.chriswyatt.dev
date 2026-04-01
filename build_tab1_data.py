"""
build_tab1_data.py
Pulls Channel Partner Overview data from BigQuery -> tab1_data.js
Includes: channel partners, customers, monthly trends, interchange by partner
"""
import os, json
from datetime import datetime, timezone

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Administrator\.openclaw\bigquery-key.json'
from google.cloud import bigquery
client = bigquery.Client(project='wyattplayground')

P = 'wyattplayground'
D = 'dbt_prod_mart_power_bi_dataset'
T  = f'`{P}.{D}.payment_metrics_full`'
TI = f'`{P}.{D}.card_interchange_report_full`'

def q(sql):
    rows = list(client.query(sql).result())
    return [dict(r) for r in rows]

# ── Channel partners with current + prior month volumes ──────────
print("Querying channel partners...")
channel_partners = q(f"""
WITH base AS (
  SELECT
    supplier_channel_partner_name                           AS channel_partner,
    COUNT(DISTINCT supplier_customer_account_name)          AS customer_count,
    COUNT(DISTINCT db_buyer_name)                           AS buyer_count,
    SUM(payment_amount)                                     AS total_volume,
    COUNT(DISTINCT payment_id)                              AS payment_count,
    SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%virtual%'
              OR LOWER(latest_disbursement_combined_payment_method) LIKE '%card%'
              THEN payment_amount ELSE 0 END)               AS vcard_volume,
    SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%ach%'
              THEN payment_amount ELSE 0 END)               AS ach_volume,
    SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%check%'
              THEN payment_amount ELSE 0 END)               AS check_volume,
    SUM(refunds_total_amount)                               AS refund_volume,
    -- current month
    SUM(CASE WHEN payment_date_created_at >= DATE_TRUNC(CURRENT_DATE(), MONTH)
              THEN payment_amount ELSE 0 END)               AS vol_this_month,
    -- prior month
    SUM(CASE WHEN payment_date_created_at >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
              AND payment_date_created_at < DATE_TRUNC(CURRENT_DATE(), MONTH)
              THEN payment_amount ELSE 0 END)               AS vol_last_month
  FROM {T}
  WHERE supplier_channel_partner_name IS NOT NULL
    AND is_internal IS NOT TRUE
  GROUP BY supplier_channel_partner_name
)
SELECT *, SAFE_DIVIDE(vol_this_month - vol_last_month, vol_last_month) * 100 AS mom_pct
FROM base
ORDER BY total_volume DESC
""")

print(f"  Got {len(channel_partners)} channel partners")

# ── Interchange by partner (net_interchange) ─────────────────────
print("Querying interchange by channel partner...")
interchange_rows = q(f"""
SELECT
  m.supplier_channel_partner_name                                   AS channel_partner,
  SUM(i.net_interchange)                                            AS net_interchange,
  SUM(CASE WHEN i.post_date >= DATE_TRUNC(CURRENT_DATE(), MONTH)
            THEN i.net_interchange ELSE 0 END)                      AS interchange_this_month,
  SUM(CASE WHEN i.post_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
            AND i.post_date < DATE_TRUNC(CURRENT_DATE(), MONTH)
            THEN i.net_interchange ELSE 0 END)                      AS interchange_last_month
FROM {TI} i
JOIN {T} m ON i.payment_id = m.payment_id
WHERE m.supplier_channel_partner_name IS NOT NULL
  AND m.is_internal IS NOT TRUE
GROUP BY channel_partner
""")
interchange_map = {r['channel_partner']: r for r in interchange_rows}

# ── Customers per top 8 partners ─────────────────────────────────
print("Querying customers per channel partner...")
top_partners = [cp['channel_partner'] for cp in channel_partners[:8]]
customers_by_partner = {}
for partner in top_partners:
    safe = partner.replace("'", "''")
    rows = q(f"""
    SELECT
      supplier_customer_account_name                  AS customer,
      COUNT(DISTINCT db_buyer_name)                   AS buyer_count,
      SUM(payment_amount)                             AS total_volume,
      COUNT(DISTINCT payment_id)                      AS payment_count,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%virtual%'
                OR LOWER(latest_disbursement_combined_payment_method) LIKE '%card%'
                THEN payment_amount ELSE 0 END)       AS vcard_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%ach%'
                THEN payment_amount ELSE 0 END)       AS ach_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%check%'
                THEN payment_amount ELSE 0 END)       AS check_volume,
      SUM(CASE WHEN payment_date_created_at >= DATE_TRUNC(CURRENT_DATE(), MONTH)
                THEN payment_amount ELSE 0 END)       AS vol_this_month,
      SUM(CASE WHEN payment_date_created_at >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
                AND payment_date_created_at < DATE_TRUNC(CURRENT_DATE(), MONTH)
                THEN payment_amount ELSE 0 END)       AS vol_last_month
    FROM {T}
    WHERE supplier_channel_partner_name = '{safe}'
      AND supplier_customer_account_name IS NOT NULL
      AND is_internal IS NOT TRUE
    GROUP BY customer
    ORDER BY total_volume DESC
    LIMIT 20
    """)
    customers_by_partner[partner] = [
        {
            'customer': r['customer'],
            'buyer_count': int(r['buyer_count'] or 0),
            'total_volume': float(r['total_volume'] or 0),
            'payment_count': int(r['payment_count'] or 0),
            'vcard_volume': float(r['vcard_volume'] or 0),
            'ach_volume': float(r['ach_volume'] or 0),
            'check_volume': float(r['check_volume'] or 0),
            'vol_this_month': float(r['vol_this_month'] or 0),
            'vol_last_month': float(r['vol_last_month'] or 0),
            'mom_pct': round(
                100 * (float(r['vol_this_month'] or 0) - float(r['vol_last_month'] or 0)) / float(r['vol_last_month'])
                if r['vol_last_month'] else 0, 1
            ),
        }
        for r in rows
    ]
    print(f"  {partner}: {len(rows)} customers")

# ── Monthly volume by partner (last 14 months) ───────────────────
print("Querying monthly volume by partner...")
monthly_by_partner = {}
for partner in top_partners:
    safe = partner.replace("'", "''")
    rows = q(f"""
    SELECT
      FORMAT_DATE('%Y-%m', payment_date_created_at)   AS month,
      SUM(payment_amount)                             AS total_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%virtual%'
                OR LOWER(latest_disbursement_combined_payment_method) LIKE '%card%'
                THEN payment_amount ELSE 0 END)       AS vcard_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%ach%'
                THEN payment_amount ELSE 0 END)       AS ach_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%check%'
                THEN payment_amount ELSE 0 END)       AS check_volume,
      COUNT(DISTINCT payment_id)                      AS payment_count
    FROM {T}
    WHERE supplier_channel_partner_name = '{safe}'
      AND payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 MONTH)
      AND is_internal IS NOT TRUE
    GROUP BY month
    ORDER BY month ASC
    """)
    monthly_by_partner[partner] = [
        {
            'month': r['month'],
            'total_volume': float(r['total_volume'] or 0),
            'vcard_volume': float(r['vcard_volume'] or 0),
            'ach_volume': float(r['ach_volume'] or 0),
            'check_volume': float(r['check_volume'] or 0),
            'payment_count': int(r['payment_count'] or 0),
        }
        for r in rows
    ]
    print(f"  {partner}: {len(rows)} months")

# ── Global monthly (all partners combined) ───────────────────────
print("Querying global monthly volume...")
global_monthly = q(f"""
SELECT
  FORMAT_DATE('%Y-%m', payment_date_created_at)   AS month,
  SUM(payment_amount)                             AS total_volume,
  SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%virtual%'
            OR LOWER(latest_disbursement_combined_payment_method) LIKE '%card%'
            THEN payment_amount ELSE 0 END)       AS vcard_volume,
  SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%ach%'
            THEN payment_amount ELSE 0 END)       AS ach_volume,
  SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%check%'
            THEN payment_amount ELSE 0 END)       AS check_volume,
  COUNT(DISTINCT payment_id)                      AS payment_count
FROM {T}
WHERE payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 MONTH)
  AND is_internal IS NOT TRUE
GROUP BY month
ORDER BY month ASC
""")
monthly_by_partner['__all__'] = [
    {
        'month': r['month'],
        'total_volume': float(r['total_volume'] or 0),
        'vcard_volume': float(r['vcard_volume'] or 0),
        'ach_volume': float(r['ach_volume'] or 0),
        'check_volume': float(r['check_volume'] or 0),
        'payment_count': int(r['payment_count'] or 0),
    }
    for r in global_monthly
]
print(f"  All partners: {len(global_monthly)} months")

# ── Assemble clean output ────────────────────────────────────────
clean_partners = []
for cp in channel_partners:
    total = float(cp['total_volume'] or 0)
    vcard = float(cp['vcard_volume'] or 0)
    ic = interchange_map.get(cp['channel_partner'], {})
    clean_partners.append({
        'channel_partner': cp['channel_partner'],
        'customer_count': int(cp['customer_count'] or 0),
        'buyer_count': int(cp['buyer_count'] or 0),
        'total_volume': total,
        'payment_count': int(cp['payment_count'] or 0),
        'vcard_volume': vcard,
        'ach_volume': float(cp['ach_volume'] or 0),
        'check_volume': float(cp['check_volume'] or 0),
        'refund_volume': float(cp['refund_volume'] or 0),
        'vcard_rate': round(100.0 * vcard / total, 1) if total else 0,
        'vol_this_month': float(cp['vol_this_month'] or 0),
        'vol_last_month': float(cp['vol_last_month'] or 0),
        'mom_pct': round(float(cp['mom_pct'] or 0), 1),
        'net_interchange': float(ic.get('net_interchange') or 0),
        'interchange_this_month': float(ic.get('interchange_this_month') or 0),
        'interchange_last_month': float(ic.get('interchange_last_month') or 0),
    })

output = {
    'channelPartners': clean_partners,
    'customersByPartner': customers_by_partner,
    'monthlyByPartner': monthly_by_partner,
    'lastUpdated': datetime.now(timezone.utc).isoformat(),
}

out_path = r'C:\Users\Administrator\.openclaw\workspace\intel-dashboard\tab1_data.js'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
with open(out_path, 'w') as f:
    f.write(f'// Auto-generated {now} UTC\n')
    f.write(f'var TAB1_DATA = {json.dumps(output, indent=2, default=str)};\n')

print(f"\nWrote {out_path}")
print(f"  {len(clean_partners)} channel partners")
print(f"  {sum(len(v) for v in customers_by_partner.values())} total customers")
