"""
build_tab1_data.py
Pulls Channel Partner Overview data from BigQuery -> tab1_data.js
v2: adds interchange earned, MoM delta data
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

print("Querying channel partners...")
channel_partners = q(f"""
SELECT
  m.supplier_channel_partner_name                           AS channel_partner,
  COUNT(DISTINCT m.supplier_customer_account_name)          AS customer_count,
  COUNT(DISTINCT m.db_buyer_name)                           AS buyer_count,
  SUM(m.payment_amount)                                     AS total_volume,
  COUNT(DISTINCT m.payment_id)                              AS payment_count,
  SUM(CASE WHEN LOWER(m.latest_disbursement_combined_payment_method) LIKE '%virtual%'
            OR LOWER(m.latest_disbursement_combined_payment_method) LIKE '%card%'
            THEN m.payment_amount ELSE 0 END)               AS vcard_volume,
  SUM(CASE WHEN LOWER(m.latest_disbursement_combined_payment_method) LIKE '%ach%'
            THEN m.payment_amount ELSE 0 END)               AS ach_volume,
  SUM(CASE WHEN LOWER(m.latest_disbursement_combined_payment_method) LIKE '%check%'
            THEN m.payment_amount ELSE 0 END)               AS check_volume,
  SUM(m.refunds_total_amount)                               AS refund_volume,
  -- Current month volume
  SUM(CASE WHEN m.payment_date_created_at >= DATE_TRUNC(CURRENT_DATE(), MONTH)
            THEN m.payment_amount ELSE 0 END)               AS vol_mtd,
  -- Prior month volume
  SUM(CASE WHEN m.payment_date_created_at >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH)
            AND m.payment_date_created_at < DATE_TRUNC(CURRENT_DATE(), MONTH)
            THEN m.payment_amount ELSE 0 END)               AS vol_prior_month,
  -- Last 30 days
  SUM(CASE WHEN m.payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            THEN m.payment_amount ELSE 0 END)               AS vol_l30,
  -- 31-60 days ago (for MoM comparison on L30)
  SUM(CASE WHEN m.payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
            AND m.payment_date_created_at < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            THEN m.payment_amount ELSE 0 END)               AS vol_l30_prior
FROM {T} m
WHERE m.supplier_channel_partner_name IS NOT NULL
  AND m.is_internal IS NOT TRUE
GROUP BY m.supplier_channel_partner_name
ORDER BY total_volume DESC
""")

print(f"  Got {len(channel_partners)} channel partners")

# Get interchange per partner
print("Querying interchange earned per channel partner...")
interchange_rows = q(f"""
SELECT
  m.supplier_channel_partner_name AS channel_partner,
  SUM(i.net_interchange)          AS net_interchange,
  SUM(i.interchange_credit)       AS interchange_credit,
  -- L30 interchange
  SUM(CASE WHEN i.post_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            THEN i.net_interchange ELSE 0 END) AS interchange_l30,
  -- Prior L30
  SUM(CASE WHEN i.post_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
            AND i.post_date < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            THEN i.net_interchange ELSE 0 END) AS interchange_l30_prior
FROM {TI} i
JOIN {T} m ON i.payment_id = m.payment_id
WHERE m.supplier_channel_partner_name IS NOT NULL
GROUP BY m.supplier_channel_partner_name
ORDER BY net_interchange DESC
""")
ic_map = {r['channel_partner']: r for r in interchange_rows}

print("Querying customers per channel partner (top 20 per partner, top 5 partners)...")
top_partners = [cp['channel_partner'] for cp in channel_partners[:5]]
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
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%check%'
                THEN payment_amount ELSE 0 END)       AS check_volume,
      SUM(CASE WHEN LOWER(latest_disbursement_combined_payment_method) LIKE '%ach%'
                THEN payment_amount ELSE 0 END)       AS ach_volume,
      -- L30
      SUM(CASE WHEN payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                THEN payment_amount ELSE 0 END)       AS vol_l30,
      SUM(CASE WHEN payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
                AND payment_date_created_at < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
                THEN payment_amount ELSE 0 END)       AS vol_l30_prior
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
            'check_volume': float(r['check_volume'] or 0),
            'ach_volume': float(r['ach_volume'] or 0),
            'vol_l30': float(r['vol_l30'] or 0),
            'vol_l30_prior': float(r['vol_l30_prior'] or 0),
        }
        for r in rows
    ]
    print(f"  {partner}: {len(rows)} customers")

print("Querying monthly volume by partner (last 13 months, top 5 partners)...")
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
      AND payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 13 MONTH)
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

# Also get aggregate monthly for "All Partners"
print("Querying aggregate monthly (all partners)...")
agg_monthly_rows = q(f"""
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
WHERE payment_date_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 13 MONTH)
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
    for r in agg_monthly_rows
]
print(f"  All partners aggregate: {len(agg_monthly_rows)} months")

# Build clean partner list with interchange
clean_partners = []
for cp in channel_partners:
    total = float(cp['total_volume'] or 0)
    vcard = float(cp['vcard_volume'] or 0)
    vol_l30 = float(cp['vol_l30'] or 0)
    vol_l30_prior = float(cp['vol_l30_prior'] or 0)
    ic = ic_map.get(cp['channel_partner'], {})
    net_ic = float(ic.get('net_interchange') or 0)
    ic_l30 = float(ic.get('interchange_l30') or 0)
    ic_l30_prior = float(ic.get('interchange_l30_prior') or 0)

    mom_pct = None
    if vol_l30_prior and vol_l30_prior > 0:
        mom_pct = round((vol_l30 - vol_l30_prior) / vol_l30_prior * 100, 1)

    ic_mom_pct = None
    if ic_l30_prior and ic_l30_prior > 0:
        ic_mom_pct = round((ic_l30 - ic_l30_prior) / ic_l30_prior * 100, 1)

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
        'vol_l30': vol_l30,
        'vol_l30_prior': vol_l30_prior,
        'mom_pct': mom_pct,
        'net_interchange': net_ic,
        'interchange_l30': ic_l30,
        'interchange_mom_pct': ic_mom_pct,
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
print(f"Partners: {len(clean_partners)}")
print(f"Interchange data for: {list(ic_map.keys())[:5]}")
