// Auto-generated 2026-03-24 17:17:49 UTC
var CBM_INSIGHTS_DATA = {
  "kpis": {
    "avg_payment_age": 13.506665581450294,
    "pct_settled": 97.53,
    "exception_rate": 0.29,
    "payments_in_flight": 42176
  },
  "ageDistribution": [
    {
      "bucket": "0-1 days",
      "count": 283648,
      "amount": 0.0
    },
    {
      "bucket": "1-3 days",
      "count": 247335,
      "amount": 0.0
    },
    {
      "bucket": "3-7 days",
      "count": 326224,
      "amount": 0.0
    },
    {
      "bucket": "7-14 days",
      "count": 550637,
      "amount": 0.0
    },
    {
      "bucket": "14-30 days",
      "count": 233113,
      "amount": 0.0
    },
    {
      "bucket": "30+ days",
      "count": 63772,
      "amount": 0.0
    }
  ],
  "eventStageFunnel": [
    {
      "stage": "Disbursement",
      "count": 1650469,
      "pct": 96.82
    },
    {
      "stage": "Reissue",
      "count": 27250,
      "pct": 1.6
    },
    {
      "stage": "Refund",
      "count": 24010,
      "pct": 1.41
    },
    {
      "stage": "Funding",
      "count": 2226,
      "pct": 0.13
    },
    {
      "stage": "Processing",
      "count": 774,
      "pct": 0.05
    }
  ],
  "exceptionTrend": [
    {
      "month": "2026-03",
      "total_payments": 397364,
      "exceptions": 1148,
      "rate": 0.29
    },
    {
      "month": "2026-02",
      "total_payments": 494754,
      "exceptions": 1430,
      "rate": 0.29
    },
    {
      "month": "2026-01",
      "total_payments": 502614,
      "exceptions": 1425,
      "rate": 0.28
    },
    {
      "month": "2025-12",
      "total_payments": 577262,
      "exceptions": 1777,
      "rate": 0.31
    },
    {
      "month": "2025-11",
      "total_payments": 513888,
      "exceptions": 1427,
      "rate": 0.28
    },
    {
      "month": "2025-10",
      "total_payments": 637093,
      "exceptions": 1611,
      "rate": 0.25
    },
    {
      "month": "2025-09",
      "total_payments": 562027,
      "exceptions": 1442,
      "rate": 0.26
    },
    {
      "month": "2025-08",
      "total_payments": 538728,
      "exceptions": 1488,
      "rate": 0.28
    },
    {
      "month": "2025-07",
      "total_payments": 560868,
      "exceptions": 2033,
      "rate": 0.36
    },
    {
      "month": "2025-06",
      "total_payments": 541328,
      "exceptions": 2238,
      "rate": 0.41
    },
    {
      "month": "2025-05",
      "total_payments": 571982,
      "exceptions": 1617,
      "rate": 0.28
    },
    {
      "month": "2025-04",
      "total_payments": 517552,
      "exceptions": 1499,
      "rate": 0.29
    }
  ],
  "refundAnalysis": {
    "total_refunds": 25427,
    "total_amount": 105659959.66000056,
    "full_count": 0,
    "partial_count": 25427,
    "by_reason": [
      {
        "reason": "AutomatedRefundCheck",
        "count": 6180,
        "amount": 11173231.150000025
      },
      {
        "reason": "RequestedByCustomer",
        "count": 4823,
        "amount": 41464221.42000004
      },
      {
        "reason": "MailReturned",
        "count": 4550,
        "amount": 16782419.44999998
      },
      {
        "reason": "Refund Requested by Customer",
        "count": 1217,
        "amount": 9197947.840000011
      },
      {
        "reason": "PartiallyUsedCard",
        "count": 1146,
        "amount": 1252467.9500000007
      },
      {
        "reason": "Undeliverable",
        "count": 925,
        "amount": 4128021.6500000013
      },
      {
        "reason": "Other",
        "count": 623,
        "amount": 706915.2099999996
      },
      {
        "reason": "PennyTest",
        "count": 585,
        "amount": 131.66999999999857
      },
      {
        "reason": "Mail Return / Undeliverable",
        "count": 440,
        "amount": 1942040.2800000007
      },
      {
        "reason": "PaymentNotAccepted",
        "count": 388,
        "amount": 1030544.9599999996
      },
      {
        "reason": "Partially Used Card",
        "count": 349,
        "amount": 299242.62000000005
      },
      {
        "reason": "AutomatedRefundCard",
        "count": 282,
        "amount": 205882.79000000007
      },
      {
        "reason": "Account Paid in Full",
        "count": 278,
        "amount": 563483.54
      },
      {
        "reason": "InvoicePaidAlready",
        "count": 184,
        "amount": 517618.00000000023
      },
      {
        "reason": "AccountPaidInFull",
        "count": 166,
        "amount": 215282.04000000007
      },
      {
        "reason": "Fraud",
        "count": 92,
        "amount": 7132365.06
      },
      {
        "reason": "Payment Not Accepted",
        "count": 72,
        "amount": 142843.19
      },
      {
        "reason": "Flagged via Payee Positive Pay",
        "count": 48,
        "amount": 550966.49
      },
      {
        "reason": "InvalidAccountNumber",
        "count": 44,
        "amount": 530348.2200000001
      },
      {
        "reason": "Automated Refund - Check",
        "count": 34,
        "amount": 31133.11
      },
      {
        "reason": "Fradulent Payment",
        "count": 32,
        "amount": 404822.9199999999
      },
      {
        "reason": "Penny Test Refund",
        "count": 27,
        "amount": 2.9999999999999964
      },
      {
        "reason": "No Account/Unable to Locate Account",
        "count": 27,
        "amount": 578333.37
      },
      {
        "reason": "PayeePositivePay",
        "count": 20,
        "amount": 68832.84
      },
      {
        "reason": "Bank Account Closed",
        "count": 10,
        "amount": 14142.670000000002
      },
      {
        "reason": "Invalid Account Number",
        "count": 8,
        "amount": 254273.41000000003
      },
      {
        "reason": "UnableToLocateAccount",
        "count": 6,
        "amount": 7059.830000000001
      },
      {
        "reason": "InternalError",
        "count": 5,
        "amount": 5159.379999999999
      },
      {
        "reason": "14",
        "count": 1,
        "amount": 160.0
      },
      {
        "reason": "BankAccountClosed",
        "count": 1,
        "amount": 2313.04
      }
    ],
    "monthly_ratio": [
      {
        "month": "2026-03",
        "payment_amount": 439777.81999999995,
        "refund_amount": 2181915.92,
        "ratio": 496.1405
      },
      {
        "month": "2026-02",
        "payment_amount": 1566652.8,
        "refund_amount": 4686285.449999997,
        "ratio": 299.1273
      },
      {
        "month": "2026-01",
        "payment_amount": 2240680.98,
        "refund_amount": 4909182.070000002,
        "ratio": 219.0933
      },
      {
        "month": "2025-12",
        "payment_amount": 2730438.2199999997,
        "refund_amount": 6388589.140000002,
        "ratio": 233.9767
      },
      {
        "month": "2025-11",
        "payment_amount": 1099801.1500000001,
        "refund_amount": 3392513.2200000025,
        "ratio": 308.4661
      },
      {
        "month": "2025-10",
        "payment_amount": 1832786.7199999997,
        "refund_amount": 4810158.080000002,
        "ratio": 262.4505
      },
      {
        "month": "2025-09",
        "payment_amount": 2723248.48,
        "refund_amount": 4524270.369999999,
        "ratio": 166.1351
      },
      {
        "month": "2025-08",
        "payment_amount": 1647531.6,
        "refund_amount": 4714258.009999998,
        "ratio": 286.1407
      },
      {
        "month": "2025-07",
        "payment_amount": 3961379.3999999994,
        "refund_amount": 9947684.52,
        "ratio": 251.1167
      },
      {
        "month": "2025-06",
        "payment_amount": 2287235.9899999998,
        "refund_amount": 4718040.350000001,
        "ratio": 206.2769
      },
      {
        "month": "2025-05",
        "payment_amount": 1582427.8,
        "refund_amount": 3743006.539999999,
        "ratio": 236.5357
      },
      {
        "month": "2025-04",
        "payment_amount": 2674810.1100000003,
        "refund_amount": 4701294.5600000005,
        "ratio": 175.7618
      }
    ]
  },
  "lastUpdated": "2026-03-24T17:17:49.666609+00:00"
};
