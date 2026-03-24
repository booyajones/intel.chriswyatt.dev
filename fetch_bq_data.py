#!/usr/bin/env python3
"""
fetch_bq_data.py

Queries Google BigQuery and outputs three JS data files for the dashboard.
Uses Application Default Credentials via google.cloud.bigquery.

Usage:
    python fetch_bq_data.py
    python fetch_bq_data.py --dry-run
    python fetch_bq_data.py --tab customer_value
    python fetch_bq_data.py --tab cbm_insights
    python fetch_bq_data.py --tab ops
"""

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone

from google.cloud import bigquery

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT = "wyattplayground"
DATASET = "dbt_prod_mart_power_bi_dataset"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def tbl(name):
    """Return a fully-qualified backtick-quoted BigQuery table reference."""
    return f"`{PROJECT}.{DATASET}.{name}`"


# ---------------------------------------------------------------------------
# BigQuery helpers
# ---------------------------------------------------------------------------

def make_client():
    return bigquery.Client(project="wyattplayground")


def run_query(client, sql, dry_run=False):
    """Execute a SQL query and return a list of dicts, or [] on error."""
    job_config = bigquery.QueryJobConfig(dry_run=dry_run)
    try:
        job = client.query(sql, job_config=job_config)
        if dry_run:
            print(f"    [dry-run] bytes processed: {job.total_bytes_processed:,}")
            return []
        rows = list(job.result())
        return [dict(row) for row in rows]
    except Exception as exc:
        print(f"    [ERROR] Query failed: {exc}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None  # None signals failure (as opposed to [] = empty result)


# ---------------------------------------------------------------------------
# JS file writer
# ---------------------------------------------------------------------------

def write_js_file(path, var_name, data):
    """Write a JS file with a header comment and a var declaration."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    header = f"// Auto-generated {now_utc} UTC\n"
    body = f"var {var_name} = {json.dumps(data, indent=2, default=str)};\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(header)
        fh.write(body)
    print(f"  Wrote {path}")


# ---------------------------------------------------------------------------
# Tab 1: customer_value_data.js
# ---------------------------------------------------------------------------

CUSTOMER_VALUE_QUERIES = {

    "kpis": f"""
SELECT
    SUM(CASE WHEN CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
             THEN payment_amount ELSE 0 END)                         AS total_payment_volume,
    COUNT(CASE WHEN CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
               THEN payment_id END)                                  AS total_payments,
    AVG(CASE WHEN CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
             THEN payment_amount END)                                AS avg_payment
FROM {tbl('pbi_star_payment_fact')}
""",

    "active_suppliers": f"""
SELECT
    COUNTIF(NG_supplier_active IS TRUE)     AS active_suppliers
FROM {tbl('pbi_dim_supplier')}
""",

    "refund_amount": f"""
SELECT
    SUM(refund_amount) AS refund_amount
FROM {tbl('pbi_dim_payment_refund')}
WHERE CAST(refund_created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
""",

    "paymentMethodMix": f"""
SELECT
    combined_payment_method AS method,
    SUM(payment_amount)     AS amount,
    COUNT(payment_id)       AS count
FROM {tbl('pbi_star_payment_fact')}
GROUP BY combined_payment_method
ORDER BY amount DESC
""",

    "monthlyVolume": f"""
SELECT
    FORMAT_DATE('%Y-%m', created_date)                          AS month,
    SUM(payment_amount)                                         AS amount,
    COUNT(payment_id)                                           AS count,
    SUM(CASE WHEN LOWER(combined_payment_method) LIKE '%ach%'
             THEN payment_amount ELSE 0 END)                   AS ach_amount,
    SUM(CASE WHEN LOWER(combined_payment_method) LIKE '%virtual%'
              OR LOWER(combined_payment_method) LIKE '%vc%'
             THEN payment_amount ELSE 0 END)                   AS vc_amount,
    SUM(CASE WHEN LOWER(combined_payment_method) LIKE '%check%'
             THEN payment_amount ELSE 0 END)                   AS check_amount
FROM {tbl('pbi_star_payment_fact')}
WHERE CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 13 MONTH)
GROUP BY month
ORDER BY month DESC
LIMIT 13
""",

    "topBuyers": f"""
SELECT
    o.buyer_name,
    SUM(o.order_payment_amount) AS amount,
    COUNT(DISTINCT o.payment_id) AS payment_count
FROM {tbl('pbi_fact_order_denorm')} o
GROUP BY o.buyer_name
ORDER BY amount DESC
LIMIT 10
""",

    "supplierStats": f"""
SELECT
    COUNTIF(NG_supplier_active IS TRUE)  AS active_count,
    COUNTIF(NG_supplier_active IS FALSE OR NG_supplier_active IS NULL) AS inactive_count
FROM {tbl('pbi_dim_supplier')}
""",

    "supplierStateDistrib": f"""
SELECT
    supplier_state_code AS state,
    COUNT(*) AS count
FROM {tbl('pbi_dim_supplier')}
WHERE supplier_state_code IS NOT NULL
GROUP BY supplier_state_code
ORDER BY count DESC
LIMIT 10
""",

    
    "supplierPropensity": f"""
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
""",

    
    "supplierPropensity": f"""
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
""",

    "supplierMethodBreakdown": f"""
SELECT
    combined_payment_method                         AS method,
    COUNT(*)                                        AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM {tbl('pbi_dim_supplier')}
WHERE combined_payment_method IS NOT NULL
GROUP BY combined_payment_method
ORDER BY count DESC
""",
}


def build_customer_value(client, dry_run=False):
    print("  Querying KPIs...")
    kpi_rows = run_query(client, CUSTOMER_VALUE_QUERIES["kpis"], dry_run)
    active_rows = run_query(client, CUSTOMER_VALUE_QUERIES["active_suppliers"], dry_run)
    refund_rows = run_query(client, CUSTOMER_VALUE_QUERIES["refund_amount"], dry_run)

    kpi_row = (kpi_rows or [{}])[0]
    active_row = (active_rows or [{}])[0]
    refund_row = (refund_rows or [{}])[0]

    kpis = {
        "total_payment_volume": float(kpi_row.get("total_payment_volume") or 0),
        "active_suppliers":     int(active_row.get("active_suppliers") or 0),
        "total_payments":       int(kpi_row.get("total_payments") or 0),
        "avg_payment":          float(kpi_row.get("avg_payment") or 0),
        "refund_amount":        float(refund_row.get("refund_amount") or 0),
    }

    print("  Querying payment method mix...")
    mix_rows = run_query(client, CUSTOMER_VALUE_QUERIES["paymentMethodMix"], dry_run) or []
    payment_method_mix = [
        {"method": r.get("method"), "amount": float(r.get("amount") or 0), "count": int(r.get("count") or 0)}
        for r in mix_rows
    ]

    print("  Querying monthly volume...")
    vol_rows = run_query(client, CUSTOMER_VALUE_QUERIES["monthlyVolume"], dry_run) or []
    monthly_volume = [
        {
            "month":       r.get("month"),
            "amount":      float(r.get("amount") or 0),
            "count":       int(r.get("count") or 0),
            "ach_amount":  float(r.get("ach_amount") or 0),
            "vc_amount":   float(r.get("vc_amount") or 0),
            "check_amount": float(r.get("check_amount") or 0),
        }
        for r in vol_rows
    ]

    print("  Querying top buyers...")
    buyer_rows = run_query(client, CUSTOMER_VALUE_QUERIES["topBuyers"], dry_run) or []
    top_buyers = [
        {"buyer_name": r.get("buyer_name"), "amount": float(r.get("amount") or 0), "payment_count": int(r.get("payment_count") or 0)}
        for r in buyer_rows
    ]

    print("  Querying supplier stats...")
    sup_rows = run_query(client, CUSTOMER_VALUE_QUERIES["supplierStats"], dry_run) or [{}]
    state_rows = run_query(client, CUSTOMER_VALUE_QUERIES["supplierStateDistrib"], dry_run) or []
    method_rows = run_query(client, CUSTOMER_VALUE_QUERIES["supplierMethodBreakdown"], dry_run) or []

    sup_row = sup_rows[0] if sup_rows else {}
    supplier_stats = {
        "active_count":       int(sup_row.get("active_count") or 0),
        "inactive_count":     int(sup_row.get("inactive_count") or 0),
        "state_distribution": [{"state": r.get("state"), "count": int(r.get("count") or 0)} for r in state_rows],
        "method_breakdown":   [
            {"method": r.get("method"), "count": int(r.get("count") or 0), "pct": float(r.get("pct") or 0)}
            for r in method_rows
        ],
    }

    
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

    return {
        "supplierPropensity": supplier_propensity,
        "kpis":              kpis,
        "paymentMethodMix":  payment_method_mix,
        "monthlyVolume":     monthly_volume,
        "topBuyers":         top_buyers,
        "supplierStats":     supplier_stats,
        "lastUpdated":       datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Tab 2: cbm_insights_data.js
# ---------------------------------------------------------------------------

CBM_INSIGHTS_QUERIES = {

    "kpis": f"""
SELECT
    AVG(CAST(payment_age AS FLOAT64))                           AS avg_payment_age,
    COUNTIF(is_payment_settled IS TRUE)                         AS settled_count,
    COUNT(*)                                                    AS total_count
FROM {tbl('pbi_payment_events_timeline_latest')} l
LEFT JOIN {tbl('pbi_payment_events_timeline_summary')} s
    ON l.BASE_RC = s.BASE_RC
""",

    "exception_rate": f"""
SELECT
    COUNT(*)                            AS total,
    COUNTIF(ple_is_exception IS TRUE)   AS exceptions
FROM {tbl('pbi_payment_events_timeline')}
WHERE CAST(event_timestamp_utc AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
""",

    "payments_in_flight": f"""
SELECT
    COUNT(*) AS payments_in_flight
FROM {tbl('pbi_payment_events_timeline_latest')}
WHERE is_payment_settled IS FALSE OR is_payment_settled IS NULL
""",

    "ageDistribution": f"""
SELECT
    CASE
        WHEN CAST(payment_age AS FLOAT64) < 1     THEN '0-1 days'
        WHEN CAST(payment_age AS FLOAT64) < 3     THEN '1-3 days'
        WHEN CAST(payment_age AS FLOAT64) < 7     THEN '3-7 days'
        WHEN CAST(payment_age AS FLOAT64) < 14    THEN '7-14 days'
        WHEN CAST(payment_age AS FLOAT64) < 30    THEN '14-30 days'
        ELSE '30+ days'
    END AS bucket,
    COUNT(*) AS count
FROM {tbl('pbi_payment_events_timeline_summary')}
WHERE payment_age IS NOT NULL
GROUP BY bucket
ORDER BY MIN(CAST(payment_age AS FLOAT64))
""",

    "ageDistributionAmount": f"""
SELECT
    CASE
        WHEN CAST(s.payment_age AS FLOAT64) < 1   THEN '0-1 days'
        WHEN CAST(s.payment_age AS FLOAT64) < 3   THEN '1-3 days'
        WHEN CAST(s.payment_age AS FLOAT64) < 7   THEN '3-7 days'
        WHEN CAST(s.payment_age AS FLOAT64) < 14  THEN '7-14 days'
        WHEN CAST(s.payment_age AS FLOAT64) < 30  THEN '14-30 days'
        ELSE '30+ days'
    END AS bucket,
    SUM(t.transaction_amount) AS amount
FROM {tbl('pbi_payment_events_timeline_summary')} s
LEFT JOIN {tbl('pbi_payment_events_timeline')} t
    ON s.BASE_RC = t.payment_id
WHERE s.payment_age IS NOT NULL
GROUP BY bucket
ORDER BY MIN(CAST(s.payment_age AS FLOAT64))
""",

    "eventStageFunnel": f"""
SELECT
    ple_event_stage                                                   AS stage,
    COUNT(*)                                                          AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)               AS pct
FROM {tbl('pbi_payment_events_timeline_latest')}
WHERE ple_event_stage IS NOT NULL
GROUP BY ple_event_stage
ORDER BY count DESC
""",

    "exceptionTrend": f"""
SELECT
    FORMAT_TIMESTAMP('%Y-%m', event_timestamp_utc)  AS month,
    COUNT(*)                                        AS total_payments,
    COUNTIF(ple_is_exception IS TRUE)               AS exceptions,
    ROUND(
        100.0 * COUNTIF(ple_is_exception IS TRUE) / NULLIF(COUNT(*), 0),
        2
    )                                               AS rate
FROM {tbl('pbi_payment_events_timeline')}
WHERE CAST(event_timestamp_utc AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month DESC
LIMIT 12
""",

    "refundAnalysis": f"""
SELECT
    COUNT(*)                                              AS total_refunds,
    SUM(refund_amount)                                    AS total_amount,
    COUNTIF(LOWER(refund_status) = 'full')                AS full_count,
    COUNTIF(LOWER(refund_status) != 'full'
            AND refund_status IS NOT NULL)                AS partial_count
FROM {tbl('pbi_dim_payment_refund')}
""",

    "refundByReason": f"""
SELECT
    refund_reason,
    COUNT(*)           AS count,
    SUM(refund_amount) AS amount
FROM {tbl('pbi_dim_payment_refund')}
WHERE refund_reason IS NOT NULL
GROUP BY refund_reason
ORDER BY count DESC
""",

    "refundMonthlyRatio": f"""
SELECT
    FORMAT_DATE('%Y-%m', r.refund_created_date)    AS month,
    SUM(r.refund_amount)                           AS refund_amount,
    SUM(p.payment_amount)                          AS payment_amount,
    ROUND(
        SAFE_DIVIDE(SUM(r.refund_amount), SUM(p.payment_amount)) * 100,
        4
    )                                              AS ratio
FROM {tbl('pbi_dim_payment_refund')} r
LEFT JOIN {tbl('pbi_star_payment_fact')} p
    ON r.payment_RC = p.business_payment_rc
    AND FORMAT_DATE('%Y-%m', r.refund_created_date) = FORMAT_DATE('%Y-%m', p.created_date)
WHERE CAST(r.refund_created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month DESC
LIMIT 12
""",
}


def build_cbm_insights(client, dry_run=False):
    print("  Querying CBM KPIs...")
    kpi_rows = run_query(client, CBM_INSIGHTS_QUERIES["kpis"], dry_run) or [{}]
    exc_rows = run_query(client, CBM_INSIGHTS_QUERIES["exception_rate"], dry_run) or [{}]
    flight_rows = run_query(client, CBM_INSIGHTS_QUERIES["payments_in_flight"], dry_run) or [{}]

    kpi_row = kpi_rows[0]
    exc_row = exc_rows[0]
    flight_row = flight_rows[0]

    total = int(kpi_row.get("total_count") or 0)
    settled = int(kpi_row.get("settled_count") or 0)
    exc_total = int(exc_row.get("total") or 0)
    exc_count = int(exc_row.get("exceptions") or 0)

    kpis = {
        "avg_payment_age":    float(kpi_row.get("avg_payment_age") or 0),
        "pct_settled":        round(100.0 * settled / total, 2) if total else 0,
        "exception_rate":     round(100.0 * exc_count / exc_total, 2) if exc_total else 0,
        "payments_in_flight": int(flight_row.get("payments_in_flight") or 0),
    }

    print("  Querying age distribution...")
    age_rows = run_query(client, CBM_INSIGHTS_QUERIES["ageDistribution"], dry_run) or []
    age_amt_rows = run_query(client, CBM_INSIGHTS_QUERIES["ageDistributionAmount"], dry_run) or []
    amt_map = {r.get("bucket"): float(r.get("amount") or 0) for r in age_amt_rows}
    age_distribution = [
        {"bucket": r.get("bucket"), "count": int(r.get("count") or 0), "amount": amt_map.get(r.get("bucket"), 0)}
        for r in age_rows
    ]

    print("  Querying event stage funnel...")
    funnel_rows = run_query(client, CBM_INSIGHTS_QUERIES["eventStageFunnel"], dry_run) or []
    event_stage_funnel = [
        {"stage": r.get("stage"), "count": int(r.get("count") or 0), "pct": float(r.get("pct") or 0)}
        for r in funnel_rows
    ]

    print("  Querying exception trend...")
    trend_rows = run_query(client, CBM_INSIGHTS_QUERIES["exceptionTrend"], dry_run) or []
    exception_trend = [
        {
            "month":          r.get("month"),
            "total_payments": int(r.get("total_payments") or 0),
            "exceptions":     int(r.get("exceptions") or 0),
            "rate":           float(r.get("rate") or 0),
        }
        for r in trend_rows
    ]

    print("  Querying refund analysis...")
    ref_rows = run_query(client, CBM_INSIGHTS_QUERIES["refundAnalysis"], dry_run) or [{}]
    reason_rows = run_query(client, CBM_INSIGHTS_QUERIES["refundByReason"], dry_run) or []
    monthly_rows = run_query(client, CBM_INSIGHTS_QUERIES["refundMonthlyRatio"], dry_run) or []

    ref_row = ref_rows[0]
    refund_analysis = {
        "total_refunds":  int(ref_row.get("total_refunds") or 0),
        "total_amount":   float(ref_row.get("total_amount") or 0),
        "full_count":     int(ref_row.get("full_count") or 0),
        "partial_count":  int(ref_row.get("partial_count") or 0),
        "by_reason": [
            {"reason": r.get("refund_reason"), "count": int(r.get("count") or 0), "amount": float(r.get("amount") or 0)}
            for r in reason_rows
        ],
        "monthly_ratio": [
            {
                "month":          r.get("month"),
                "payment_amount": float(r.get("payment_amount") or 0),
                "refund_amount":  float(r.get("refund_amount") or 0),
                "ratio":          float(r.get("ratio") or 0),
            }
            for r in monthly_rows
        ],
    }

    
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

    return {
        "supplierPropensity": supplier_propensity,
        "kpis":            kpis,
        "ageDistribution": age_distribution,
        "eventStageFunnel": event_stage_funnel,
        "exceptionTrend":  exception_trend,
        "refundAnalysis":  refund_analysis,
        "lastUpdated":     datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Tab 3: ops_data.js
# ---------------------------------------------------------------------------

OPS_QUERIES = {

    "kpis_processing": f"""
SELECT COUNT(*) AS payments_processing
FROM {tbl('pbi_payment_events_timeline_latest')}
WHERE is_payment_settled IS FALSE OR is_payment_settled IS NULL
""",

    "kpis_exceptions": f"""
SELECT COUNT(*) AS exceptions_open
FROM {tbl('pbi_payment_events_timeline_latest')}
WHERE ple_event_stage IS NOT NULL
  AND (is_payment_settled IS FALSE OR is_payment_settled IS NULL)
  AND ple_event_name LIKE '%exception%'
""",

    "kpis_refunds": f"""
SELECT COUNT(*) AS refunds_pending
FROM {tbl('pbi_dim_payment_refund')}
WHERE LOWER(refund_status) NOT IN ('settled', 'completed', 'paid')
  AND refund_status IS NOT NULL
""",

    "kpis_cases": f"""
SELECT
    COUNT(*)                                                   AS total_cases,
    COUNTIF(LOWER(status) IN ('closed', 'resolved'))           AS closed_cases
FROM {tbl('pbi_sf_case')}
""",

    "paymentStatus": f"""
SELECT
    p.payment_platform_status                                      AS status,
    COUNT(*)                                                       AS count,
    SUM(p.payment_amount)                                          AS amount,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)            AS pct
FROM {tbl('pbi_star_payment_fact')} p
WHERE p.payment_platform_status IS NOT NULL
GROUP BY p.payment_platform_status
ORDER BY count DESC
""",

    "deliveryMethodTrend": f"""
SELECT
    FORMAT_DATE('%Y-%m', created_date)                             AS month,
    SUM(CASE WHEN LOWER(latest_payment_delivery_method) LIKE '%ach%'
             THEN 1 ELSE 0 END)                                   AS ach,
    SUM(CASE WHEN LOWER(latest_payment_delivery_method) LIKE '%virtual%'
              OR LOWER(latest_payment_delivery_method) LIKE '%vc%'
             THEN 1 ELSE 0 END)                                   AS virtual_card,
    SUM(CASE WHEN LOWER(latest_payment_delivery_method) LIKE '%check%'
             THEN 1 ELSE 0 END)                                   AS check,
    SUM(CASE WHEN LOWER(latest_payment_delivery_method) NOT LIKE '%ach%'
              AND LOWER(latest_payment_delivery_method) NOT LIKE '%virtual%'
              AND LOWER(latest_payment_delivery_method) NOT LIKE '%vc%'
              AND LOWER(latest_payment_delivery_method) NOT LIKE '%check%'
             THEN 1 ELSE 0 END)                                   AS other
FROM {tbl('pbi_star_payment_fact')}
WHERE CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  AND latest_payment_delivery_method IS NOT NULL
GROUP BY month
ORDER BY month DESC
LIMIT 12
""",

    "paymentEventTimeline": f"""
SELECT
    ple_event_name                                                AS event_name,
    COUNT(*)                                                      AS count,
    ROUND(
        AVG(TIMESTAMP_DIFF(event_timestamp_utc, event_timestamp_utc, HOUR)),
        2
    )                                                             AS avg_hours_to_event
FROM {tbl('pbi_payment_events_timeline')}
WHERE ple_event_name IS NOT NULL
GROUP BY ple_event_name
ORDER BY avg_hours_to_event
""",

    "caseByType": f"""
SELECT
    type,
    COUNT(*)                                                      AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)           AS pct
FROM {tbl('pbi_sf_case')}
WHERE type IS NOT NULL
GROUP BY type
ORDER BY count DESC
""",

    "caseByStatus": f"""
SELECT
    status,
    COUNT(*) AS count
FROM {tbl('pbi_sf_case')}
WHERE status IS NOT NULL
GROUP BY status
ORDER BY count DESC
""",

    "caseResolutionDays": f"""
SELECT
    AVG(child_case_time_in_days_c) AS avg_resolution_days
FROM {tbl('pbi_sf_case')}
WHERE child_case_time_in_days_c IS NOT NULL
""",

    "caseMonthlyVolume": f"""
SELECT
    FORMAT_DATE('%Y-%m', created_date)                              AS month,
    COUNT(*)                                                        AS new_cases,
    COUNTIF(LOWER(status) IN ('closed', 'resolved'))               AS closed_cases
FROM {tbl('pbi_sf_case')}
WHERE CAST(created_date AS DATE) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month DESC
LIMIT 12
""",

    "refundDetails": f"""
SELECT
    refund_reason,
    COUNT(*)           AS count,
    SUM(refund_amount) AS total_amount,
    AVG(refund_amount) AS avg_amount
FROM {tbl('pbi_dim_payment_refund')}
WHERE refund_reason IS NOT NULL
GROUP BY refund_reason
ORDER BY total_amount DESC
""",

    "checkProcessing": f"""
SELECT
    COUNT(*)                                                             AS total_checks,
    COUNTIF(LOWER(payment_platform_status) NOT IN ('invalid', 'failed',
            'returned', 'rejected'))                                     AS valid_count,
    COUNTIF(LOWER(payment_platform_status) IN ('invalid', 'failed',
            'returned', 'rejected'))                                     AS invalid_count,
    AVG(payment_amount)                                                  AS avg_amount
FROM {tbl('pbi_star_payment_fact')}
WHERE LOWER(latest_payment_delivery_method) LIKE '%check%'
""",
}


def build_ops(client, dry_run=False):
    print("  Querying Ops KPIs...")
    proc_rows   = run_query(client, OPS_QUERIES["kpis_processing"], dry_run) or [{}]
    exc_rows    = run_query(client, OPS_QUERIES["kpis_exceptions"], dry_run) or [{}]
    ref_rows    = run_query(client, OPS_QUERIES["kpis_refunds"], dry_run) or [{}]
    case_rows   = run_query(client, OPS_QUERIES["kpis_cases"], dry_run) or [{}]

    case_row = case_rows[0]
    total_cases  = int(case_row.get("total_cases") or 0)
    closed_cases = int(case_row.get("closed_cases") or 0)

    kpis = {
        "payments_processing":  int((proc_rows[0] or {}).get("payments_processing") or 0),
        "exceptions_open":      int((exc_rows[0] or {}).get("exceptions_open") or 0),
        "refunds_pending":      int((ref_rows[0] or {}).get("refunds_pending") or 0),
        "case_resolution_rate": round(100.0 * closed_cases / total_cases, 2) if total_cases else 0,
    }

    print("  Querying payment status breakdown...")
    status_rows = run_query(client, OPS_QUERIES["paymentStatus"], dry_run) or []
    payment_status = [
        {
            "status": r.get("status"),
            "count":  int(r.get("count") or 0),
            "amount": float(r.get("amount") or 0),
            "pct":    float(r.get("pct") or 0),
        }
        for r in status_rows
    ]

    print("  Querying delivery method trend...")
    delivery_rows = run_query(client, OPS_QUERIES["deliveryMethodTrend"], dry_run) or []
    delivery_method_trend = [
        {
            "month":        r.get("month"),
            "ach":          int(r.get("ach") or 0),
            "virtual_card": int(r.get("virtual_card") or 0),
            "check":        int(r.get("check") or 0),
            "other":        int(r.get("other") or 0),
        }
        for r in delivery_rows
    ]

    print("  Querying payment event timeline...")
    timeline_rows = run_query(client, OPS_QUERIES["paymentEventTimeline"], dry_run) or []
    payment_event_timeline = [
        {
            "event_name":       r.get("event_name"),
            "count":            int(r.get("count") or 0),
            "avg_hours_to_event": float(r.get("avg_hours_to_event") or 0),
        }
        for r in timeline_rows
    ]

    print("  Querying case breakdown...")
    type_rows   = run_query(client, OPS_QUERIES["caseByType"], dry_run) or []
    status_case = run_query(client, OPS_QUERIES["caseByStatus"], dry_run) or []
    res_rows    = run_query(client, OPS_QUERIES["caseResolutionDays"], dry_run) or [{}]
    monthly_case = run_query(client, OPS_QUERIES["caseMonthlyVolume"], dry_run) or []

    case_breakdown = {
        "by_type":  [
            {"type": r.get("type"), "count": int(r.get("count") or 0), "pct": float(r.get("pct") or 0)}
            for r in type_rows
        ],
        "by_status": [
            {"status": r.get("status"), "count": int(r.get("count") or 0)}
            for r in status_case
        ],
        "avg_resolution_days": float((res_rows[0] or {}).get("avg_resolution_days") or 0),
        "monthly_volume": [
            {
                "month":       r.get("month"),
                "new_cases":   int(r.get("new_cases") or 0),
                "closed_cases": int(r.get("closed_cases") or 0),
            }
            for r in monthly_case
        ],
    }

    print("  Querying refund details...")
    refund_rows = run_query(client, OPS_QUERIES["refundDetails"], dry_run) or []
    refund_details = [
        {
            "refund_reason": r.get("refund_reason"),
            "count":         int(r.get("count") or 0),
            "total_amount":  float(r.get("total_amount") or 0),
            "avg_amount":    float(r.get("avg_amount") or 0),
        }
        for r in refund_rows
    ]

    print("  Querying check processing stats...")
    check_rows = run_query(client, OPS_QUERIES["checkProcessing"], dry_run) or [{}]
    check_row = check_rows[0]
    check_processing = {
        "total_checks":  int(check_row.get("total_checks") or 0),
        "valid_count":   int(check_row.get("valid_count") or 0),
        "invalid_count": int(check_row.get("invalid_count") or 0),
        "avg_amount":    float(check_row.get("avg_amount") or 0),
    }

    
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

    return {
        "supplierPropensity": supplier_propensity,
        "kpis":                 kpis,
        "paymentStatus":        payment_status,
        "deliveryMethodTrend":  delivery_method_trend,
        "paymentEventTimeline": payment_event_timeline,
        "caseBreakdown":        case_breakdown,
        "refundDetails":        refund_details,
        "checkProcessing":      check_processing,
        "lastUpdated":          datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

TABS = {
    "customer_value": {
        "build_fn":  build_customer_value,
        "js_file":   "customer_value_data.js",
        "var_name":  "CUSTOMER_VALUE_DATA",
    },
    "cbm_insights": {
        "build_fn":  build_cbm_insights,
        "js_file":   "cbm_insights_data.js",
        "var_name":  "CBM_INSIGHTS_DATA",
    },
    "ops": {
        "build_fn":  build_ops,
        "js_file":   "ops_data.js",
        "var_name":  "OPS_DATA",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Fetch BigQuery data and write dashboard JS data files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate queries without executing them (uses BigQuery dry-run mode).",
    )
    parser.add_argument(
        "--tab",
        choices=list(TABS.keys()),
        default=None,
        help="Only regenerate a specific tab. Omit to regenerate all tabs.",
    )
    args = parser.parse_args()

    tabs_to_run = [args.tab] if args.tab else list(TABS.keys())

    print(f"Initializing BigQuery client (project={PROJECT})...")
    try:
        client = make_client()
    except Exception as exc:
        print(f"[FATAL] Could not create BigQuery client: {exc}", file=sys.stderr)
        sys.exit(1)

    any_error = False
    for tab_key in tabs_to_run:
        tab = TABS[tab_key]
        print(f"\n[{tab_key}] Building {tab['js_file']}...")
        try:
            data = tab["build_fn"](client, dry_run=args.dry_run)
            if not args.dry_run:
                out_path = os.path.join(SCRIPT_DIR, tab["js_file"])
                write_js_file(out_path, tab["var_name"], data)
            else:
                print(f"  [dry-run] Skipping file write for {tab['js_file']}")
        except Exception as exc:
            print(f"  [ERROR] Failed to build {tab_key}: {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            any_error = True

    if any_error:
        print("\nCompleted with errors.")
        sys.exit(1)
    else:
        print("\nDone.")


if __name__ == "__main__":
    main()



