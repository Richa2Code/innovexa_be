"""
Static seed data for NSFDC (National Scheduled Castes Finance and
Development Corporation) schemes.

Source: https://nsfdc.nic.in/scheme (verified 2026-09-05)

Each top-level entry maps directly onto the `Scheme` model's columns.
Each dict in `repayment_rules` maps directly onto the
`SchemeRepaymentRule` model's columns (scheme_id is added at seed time).

Note: NSFDC revised its scheme portfolio effective 01.10.2023. Older
standalone schemes (Mahila Samriddhi Yojana, Mahila Kisan Yojana, Shilpi
Samriddhi Yojana, Laghu Vyavasay Yojana) were discontinued/merged into the
5 schemes below and are intentionally omitted. NSFDC also sponsors a
non-credit Skill Development scheme under PM-DAKSH Yojana, which is
excluded here since it has no loan/interest/repayment terms.
"""

NSFDC_SCHEMES = [
    {
        "name": "Micro Finance Scheme (MFS)",
        "code": "NSFDC-MFS",
        "category": "Micro Finance",
        "purpose": "To support small/micro business activities for units costing up to Rs. 1.40 lakh",
        "description": (
            "NSFDC provides Micro Credit Finance for units costing up to "
            "Rs. 1.40 lakh, extended through State/UT Channelising Agencies "
            "(SCAs/CAs), to enable eligible Scheduled Caste persons to set "
            "up or expand income-generating activities."
        ),
        "min_project_cost": 0,
        "max_project_cost": 140000,
        "finance_percentage": 90,
        "max_loan_amount": 125000,
        "nsfdc_interest_rate": 2.5,
        "beneficiary_interest_rate": 6.5,
        "source_url": "https://nsfdc.nic.in/en/micro-credit-finance",
        "repayment_rules": [
            {
                "repayment_frequency": "Quarterly",
                "max_repayment_period": "3 years",
                "moratorium_period": "3 months",
                "condition": (
                    "Repaid in quarterly instalments within a maximum "
                    "period of three years from the date of disbursement, "
                    "including a 3-month moratorium period."
                ),
            },
        ],
    },
    {
        "name": "Term Loan",
        "code": "NSFDC-TL",
        "category": "Term Loan",
        "purpose": "To support units costing more than Rs. 1.40 lakh and up to Rs. 50 lakh",
        "description": (
            "NSFDC provides Term Loans, above the Micro Finance Scheme "
            "ceiling, for units costing more than Rs. 1.40 lakh and up to "
            "Rs. 50 lakh, extended through SCAs/CAs."
        ),
        "min_project_cost": 140000,
        "max_project_cost": 5000000,
        "finance_percentage": 90,
        "max_loan_amount": 4500000,
        "nsfdc_interest_rate": 4,
        "beneficiary_interest_rate": 8,
        "source_url": "https://nsfdc.nic.in/en/term-loan",
        "repayment_rules": [
            {
                "repayment_frequency": "Quarterly",
                "max_repayment_period": "7 years",
                "moratorium_period": (
                    "6 months (12 months for plantation and construction "
                    "activities)"
                ),
                "condition": (
                    "Repaid in quarterly instalments within seven years, "
                    "including a 6-month moratorium (12 months for "
                    "plantation and construction activities)."
                ),
            },
        ],
    },
    {
        "name": "Aajeevika Micro-Finance Yojana",
        "code": "NSFDC-AMY",
        "category": "Micro Finance (via NBFC-MFI)",
        "purpose": "Need-based micro finance for small/micro business activities through NBFC-MFIs",
        "description": (
            "NSFDC provides prompt, need-based micro finance to eligible "
            "Scheduled Caste persons at reasonable interest rates through "
            "selected NBFC-MFIs to pursue small/micro business activities, "
            "for projects costing up to Rs. 1.40 lakh."
        ),
        "min_project_cost": 0,
        "max_project_cost": 140000,
        "finance_percentage": 90,
        "max_loan_amount": 125000,
        "nsfdc_interest_rate": 5,
        "beneficiary_interest_rate": 15,
        "source_url": "https://nsfdc.nic.in/scheme",
        "repayment_rules": [
            {
                "repayment_frequency": "Quarterly",
                "max_repayment_period": "3 years",
                "moratorium_period": "3 months",
                "condition": (
                    "Repaid in quarterly instalments of up to three years "
                    "from the date of each disbursement, including a "
                    "3-month moratorium period."
                ),
            },
        ],
    },
    {
        "name": "Udyam Nidhi Yojana (UNY)",
        "code": "NSFDC-UNY",
        "category": "Micro Finance (via Cooperative Banks/Societies & Small Finance Banks)",
        "purpose": "To support small/micro activities for projects/units costing up to Rs. 5 lakh",
        "description": (
            "NSFDC provides loans under Udyam Nidhi Yojana for "
            "projects/units costing up to Rs. 5 lakh through Cooperative "
            "Societies, Cooperative Banks, and Small Finance Banks (SFBs). "
            "NSFDC charges 5% p.a. from the channelising institution in "
            "both cases; beneficiaries served via Cooperative "
            "Banks/Societies pay 13% p.a., while beneficiaries served via "
            "Small Finance Banks pay 15% p.a."
        ),
        "min_project_cost": 0,
        "max_project_cost": 500000,
        "finance_percentage": 90,
        "max_loan_amount": 450000,
        "nsfdc_interest_rate": 5,
        # NOTE: model has a single beneficiary_interest_rate column; the
        # scheme actually has two beneficiary rates depending on channel
        # (13% via Co-op Banks/Societies, 15% via Small Finance Banks).
        # The lower (Co-op) rate is stored here; the full breakdown is in
        # `description`.
        "beneficiary_interest_rate": 13,
        "source_url": "https://nsfdc.nic.in/scheme",
        "repayment_rules": [
            {
                "repayment_frequency": "Quarterly or Half-yearly",
                "max_repayment_period": "5 years",
                "moratorium_period": "3 months",
                "condition": (
                    "Repaid in quarterly or half-yearly instalments "
                    "within a maximum period of up to 5 years, including "
                    "a 3-month moratorium period."
                ),
            },
        ],
    },
    {
        "name": "Educational Loan Scheme (ELS)",
        "code": "NSFDC-ELS",
        "category": "Education Loan",
        "purpose": "To fund regular full-time professional/technical recognized courses in India or abroad",
        "description": (
            "Educational Loan provided to eligible Scheduled Caste students "
            "for pursuing regular full-time professional / technical "
            "courses recognized/approved by the Government, in India or "
            "abroad. Loan amount up to Rs. 40 lakh or 90% of course fee, "
            "whichever is less. Covers courses such as Engineering, "
            "Medicine, Architecture, Pharmacy, Law, Management, Nursing, "
            "IT, Chartered Accountancy, and doctoral studies (M.Phil/PhD), "
            "among others."
        ),
        "min_project_cost": 0,
        "max_project_cost": 4000000,
        "finance_percentage": 90,
        "max_loan_amount": 3600000,
        "nsfdc_interest_rate": 2.5,
        "beneficiary_interest_rate": 6.5,
        "source_url": "https://nsfdc.nic.in/scheme",
        "repayment_rules": [
            {
                "repayment_frequency": "As applicable",
                "max_repayment_period": "12 years",
                "moratorium_period": "Course period plus 1 year",
                "condition": "Applicable where repayment has not started.",
            },
            {
                "repayment_frequency": "As applicable",
                "max_repayment_period": "10 years",
                "moratorium_period": "6 months",
                "condition": (
                    "Applicable where loan has been disbursed and "
                    "repayment has already started."
                ),
            },
        ],
    },
]

# ------------------------------------------------------------------------
# Discontinued / not-applicable schemes (for reference only, NOT seeded):
#
# - Mahila Samriddhi Yojana, Mahila Kisan Yojana, Shilpi Samriddhi Yojana,
#   Laghu Vyavasay Yojana: standalone NSFDC schemes discontinued/merged
#   into the current lineup after NSFDC's scheme revision effective
#   01.10.2023.
# - "Mahila Adhikarita Yojana": belongs to NSKFDC (National Safai
#   Karamcharis Finance & Development Corporation) - a different
#   corporation for Safai Karamcharis/sanitation workers, not NSFDC.
# - Skill Development Training under PM-DAKSH Yojana: a non-credit NSFDC
#   scheme with no project cost/interest/repayment terms, so it doesn't
#   fit the Scheme/SchemeRepaymentRule schema and is excluded here.
# ------------------------------------------------------------------------