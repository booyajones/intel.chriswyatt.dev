// Auto-generated 2026-03-24 17:17:59 UTC
var OPS_DATA = {
  "kpis": {
    "payments_processing": 42176,
    "exceptions_open": 0,
    "refunds_pending": 25427,
    "case_resolution_rate": 98.84
  },
  "paymentStatus": [
    {
      "status": "Settled",
      "count": 1683509,
      "amount": 12160152546.40013,
      "pct": 98.76
    },
    {
      "status": "In Progress",
      "count": 21219,
      "amount": 104296512.66000003,
      "pct": 1.24
    },
    {
      "status": "Voided",
      "count": 1,
      "amount": 1.5,
      "pct": 0.0
    }
  ],
  "deliveryMethodTrend": [
    {
      "month": "2026-03",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 45582
    },
    {
      "month": "2026-02",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 56564
    },
    {
      "month": "2026-01",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 58965
    },
    {
      "month": "2025-12",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 66118
    },
    {
      "month": "2025-11",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 59425
    },
    {
      "month": "2025-10",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 74593
    },
    {
      "month": "2025-09",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 67257
    },
    {
      "month": "2025-08",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 66809
    },
    {
      "month": "2025-07",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 70740
    },
    {
      "month": "2025-06",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 67199
    },
    {
      "month": "2025-05",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 74344
    },
    {
      "month": "2025-04",
      "ach": 0,
      "virtual_card": 0,
      "check": 0,
      "other": 68033
    }
  ],
  "paymentEventTimeline": [
    {
      "event_name": "sent",
      "count": 1139403,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "stop_confirmed",
      "count": 23718,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "undeliverable",
      "count": 1395,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "requested",
      "count": 3434287,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "received",
      "count": 1703245,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "load",
      "count": 503027,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "cleared",
      "count": 730287,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "voided",
      "count": 7036,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "sent_to_printer",
      "count": 68095,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "return_to_sender",
      "count": 3267,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "rerouted",
      "count": 3218,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "returned",
      "count": 5465,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "reversed",
      "count": 23,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "reverse_pospay",
      "count": 6,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "completed",
      "count": 499048,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "unload",
      "count": 28051,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "mailed",
      "count": 777553,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "initiated",
      "count": 21881,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "stop_processing",
      "count": 1242,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "failed",
      "count": 94,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "confirmed",
      "count": 1704626,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "purchase",
      "count": 510748,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "issued",
      "count": 742424,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "printed",
      "count": 762125,
      "avg_hours_to_event": 0.0
    },
    {
      "event_name": "stop_requested",
      "count": 23720,
      "avg_hours_to_event": 0.0
    }
  ],
  "caseBreakdown": {
    "by_type": [
      {
        "type": "Internal Payment",
        "count": 126797,
        "pct": 68.75
      },
      {
        "type": "Exception",
        "count": 25506,
        "pct": 13.83
      },
      {
        "type": "Enrollment Delay",
        "count": 7467,
        "pct": 4.05
      },
      {
        "type": "Payment Question",
        "count": 5213,
        "pct": 2.83
      },
      {
        "type": "Supplier Updates",
        "count": 4760,
        "pct": 2.58
      },
      {
        "type": "Customer Ops SE Request",
        "count": 3891,
        "pct": 2.11
      },
      {
        "type": "task",
        "count": 1897,
        "pct": 1.03
      },
      {
        "type": "Payment Dispute",
        "count": 1846,
        "pct": 1.0
      },
      {
        "type": "Payment Delay",
        "count": 1669,
        "pct": 0.9
      },
      {
        "type": "Ticket",
        "count": 1183,
        "pct": 0.64
      },
      {
        "type": "vCard Retention Request",
        "count": 1020,
        "pct": 0.55
      },
      {
        "type": "General",
        "count": 439,
        "pct": 0.24
      },
      {
        "type": "Profile Change",
        "count": 382,
        "pct": 0.21
      },
      {
        "type": "Supplier Profile Update",
        "count": 329,
        "pct": 0.18
      },
      {
        "type": "Question",
        "count": 292,
        "pct": 0.16
      },
      {
        "type": "Problem",
        "count": 257,
        "pct": 0.14
      },
      {
        "type": "Banking Change",
        "count": 211,
        "pct": 0.11
      },
      {
        "type": "Funding Due Diligence",
        "count": 186,
        "pct": 0.1
      },
      {
        "type": "ACH Exception",
        "count": 167,
        "pct": 0.09
      },
      {
        "type": "Legal Due Diligence",
        "count": 155,
        "pct": 0.08
      },
      {
        "type": "Finexio Portal Question",
        "count": 120,
        "pct": 0.07
      },
      {
        "type": "Check Exception",
        "count": 120,
        "pct": 0.07
      },
      {
        "type": "Finexio Client/Buyer Updates",
        "count": 117,
        "pct": 0.06
      },
      {
        "type": "Change Request",
        "count": 111,
        "pct": 0.06
      },
      {
        "type": "Client Updates",
        "count": 105,
        "pct": 0.06
      },
      {
        "type": "Portal Question",
        "count": 68,
        "pct": 0.04
      },
      {
        "type": "Profile and Banking Change",
        "count": 57,
        "pct": 0.03
      },
      {
        "type": "Supplier vCard Lead",
        "count": 16,
        "pct": 0.01
      },
      {
        "type": "Client Profile Update",
        "count": 12,
        "pct": 0.01
      },
      {
        "type": "Project Request",
        "count": 12,
        "pct": 0.01
      },
      {
        "type": "Feature Request",
        "count": 10,
        "pct": 0.01
      },
      {
        "type": "Incident",
        "count": 6,
        "pct": 0.0
      },
      {
        "type": "Complete with DocuSign: Change Management Forms (Profile).pdf",
        "count": 2,
        "pct": 0.0
      },
      {
        "type": "vCard At Risk Retention Opportunity",
        "count": 2,
        "pct": 0.0
      },
      {
        "type": "Complete with DocuSign: Zendesk x Salesforce Requirements Updated 12.6.pdf",
        "count": 1,
        "pct": 0.0
      },
      {
        "type": "this",
        "count": 1,
        "pct": 0.0
      },
      {
        "type": "ACH Request",
        "count": 1,
        "pct": 0.0
      }
    ],
    "by_status": [
      {
        "status": "Closed",
        "count": 208137
      },
      {
        "status": "Completed",
        "count": 1189
      },
      {
        "status": "Pending Information",
        "count": 893
      },
      {
        "status": "In Progress",
        "count": 189
      },
      {
        "status": "New",
        "count": 82
      },
      {
        "status": "Closed Expired",
        "count": 41
      },
      {
        "status": "Pending Action",
        "count": 32
      },
      {
        "status": "Information Received",
        "count": 8
      },
      {
        "status": "Additional Investigation",
        "count": 2
      },
      {
        "status": "Cancelled",
        "count": 1
      }
    ],
    "avg_resolution_days": 0.4090663614691229,
    "monthly_volume": [
      {
        "month": "2026-03",
        "new_cases": 3938,
        "closed_cases": 3576
      },
      {
        "month": "2026-02",
        "new_cases": 5424,
        "closed_cases": 5290
      },
      {
        "month": "2026-01",
        "new_cases": 5245,
        "closed_cases": 5166
      },
      {
        "month": "2025-12",
        "new_cases": 5521,
        "closed_cases": 5450
      },
      {
        "month": "2025-11",
        "new_cases": 5352,
        "closed_cases": 5309
      },
      {
        "month": "2025-10",
        "new_cases": 7316,
        "closed_cases": 7254
      },
      {
        "month": "2025-09",
        "new_cases": 6216,
        "closed_cases": 6169
      },
      {
        "month": "2025-08",
        "new_cases": 5825,
        "closed_cases": 5731
      },
      {
        "month": "2025-07",
        "new_cases": 6439,
        "closed_cases": 6390
      },
      {
        "month": "2025-06",
        "new_cases": 6004,
        "closed_cases": 5965
      },
      {
        "month": "2025-05",
        "new_cases": 6586,
        "closed_cases": 6500
      },
      {
        "month": "2025-04",
        "new_cases": 5644,
        "closed_cases": 5626
      }
    ]
  },
  "refundDetails": [
    {
      "refund_reason": "RequestedByCustomer",
      "count": 4823,
      "total_amount": 41464221.42000004,
      "avg_amount": 8597.184619531381
    },
    {
      "refund_reason": "MailReturned",
      "count": 4550,
      "total_amount": 16782419.44999998,
      "avg_amount": 3688.4438351648478
    },
    {
      "refund_reason": "AutomatedRefundCheck",
      "count": 6180,
      "total_amount": 11173231.150000025,
      "avg_amount": 1807.9662055016183
    },
    {
      "refund_reason": "Refund Requested by Customer",
      "count": 1217,
      "total_amount": 9197947.840000011,
      "avg_amount": 7557.886474938379
    },
    {
      "refund_reason": "Fraud",
      "count": 92,
      "total_amount": 7132365.06,
      "avg_amount": 77525.70717391306
    },
    {
      "refund_reason": "Undeliverable",
      "count": 925,
      "total_amount": 4128021.6500000013,
      "avg_amount": 4462.726108108106
    },
    {
      "refund_reason": "Mail Return / Undeliverable",
      "count": 440,
      "total_amount": 1942040.2800000007,
      "avg_amount": 4413.727909090909
    },
    {
      "refund_reason": "PartiallyUsedCard",
      "count": 1146,
      "total_amount": 1252467.9500000007,
      "avg_amount": 1092.9039703315898
    },
    {
      "refund_reason": "PaymentNotAccepted",
      "count": 388,
      "total_amount": 1030544.9599999996,
      "avg_amount": 2656.043711340206
    },
    {
      "refund_reason": "Other",
      "count": 623,
      "total_amount": 706915.2099999996,
      "avg_amount": 1134.695361155699
    },
    {
      "refund_reason": "No Account/Unable to Locate Account",
      "count": 27,
      "total_amount": 578333.37,
      "avg_amount": 21419.754444444447
    },
    {
      "refund_reason": "Account Paid in Full",
      "count": 278,
      "total_amount": 563483.54,
      "avg_amount": 2026.9192086330943
    },
    {
      "refund_reason": "Flagged via Payee Positive Pay",
      "count": 48,
      "total_amount": 550966.49,
      "avg_amount": 11478.468541666667
    },
    {
      "refund_reason": "InvalidAccountNumber",
      "count": 44,
      "total_amount": 530348.2200000001,
      "avg_amount": 12053.368636363633
    },
    {
      "refund_reason": "InvoicePaidAlready",
      "count": 184,
      "total_amount": 517618.00000000023,
      "avg_amount": 2813.1413043478237
    },
    {
      "refund_reason": "Fradulent Payment",
      "count": 32,
      "total_amount": 404822.9199999999,
      "avg_amount": 12650.71625
    },
    {
      "refund_reason": "Partially Used Card",
      "count": 349,
      "total_amount": 299242.62000000005,
      "avg_amount": 857.4287106017186
    },
    {
      "refund_reason": "Invalid Account Number",
      "count": 8,
      "total_amount": 254273.41000000003,
      "avg_amount": 31784.17625
    },
    {
      "refund_reason": "AccountPaidInFull",
      "count": 166,
      "total_amount": 215282.04000000007,
      "avg_amount": 1296.879759036145
    },
    {
      "refund_reason": "AutomatedRefundCard",
      "count": 282,
      "total_amount": 205882.79000000007,
      "avg_amount": 730.080815602837
    },
    {
      "refund_reason": "Payment Not Accepted",
      "count": 72,
      "total_amount": 142843.19,
      "avg_amount": 1983.9331944444446
    },
    {
      "refund_reason": "PayeePositivePay",
      "count": 20,
      "total_amount": 68832.84,
      "avg_amount": 3441.6420000000003
    },
    {
      "refund_reason": "Automated Refund - Check",
      "count": 34,
      "total_amount": 31133.11,
      "avg_amount": 915.6797058823529
    },
    {
      "refund_reason": "Bank Account Closed",
      "count": 10,
      "total_amount": 14142.670000000002,
      "avg_amount": 1414.267
    },
    {
      "refund_reason": "UnableToLocateAccount",
      "count": 6,
      "total_amount": 7059.830000000001,
      "avg_amount": 1176.6383333333333
    },
    {
      "refund_reason": "InternalError",
      "count": 5,
      "total_amount": 5159.379999999999,
      "avg_amount": 1031.8759999999997
    },
    {
      "refund_reason": "BankAccountClosed",
      "count": 1,
      "total_amount": 2313.04,
      "avg_amount": 2313.04
    },
    {
      "refund_reason": "14",
      "count": 1,
      "total_amount": 160.0,
      "avg_amount": 160.0
    },
    {
      "refund_reason": "PennyTest",
      "count": 585,
      "total_amount": 131.66999999999857,
      "avg_amount": 0.2250769230769233
    },
    {
      "refund_reason": "Penny Test Refund",
      "count": 27,
      "total_amount": 2.9999999999999964,
      "avg_amount": 0.11111111111111115
    }
  ],
  "checkProcessing": {
    "total_checks": 0,
    "valid_count": 0,
    "invalid_count": 0,
    "avg_amount": 0.0
  },
  "lastUpdated": "2026-03-24T17:17:59.067808+00:00"
};
