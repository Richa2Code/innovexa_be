from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator

class CountryResponse(BaseModel):
    id: str
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)


class StateResponse(BaseModel):
    id: str
    name: str
    country_id: str

    model_config = ConfigDict(from_attributes=True)


class DistrictResponse(BaseModel):
    id: str
    name: str
    state_id: str

    model_config = ConfigDict(from_attributes=True)


class SchemeEligibilityRequest(BaseModel):
    purpose: str
    project_cost: Optional[float] = None
    annual_income: Optional[float] = None
    category: Optional[str] = None
    state_id: Optional[str] = None
    district_id: Optional[str] = None

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, v: str) -> str:
        allowed = ["Term Loan", "Education Loan", "Micro Finance"]
        if v not in allowed:
            raise ValueError(f"purpose must be one of {allowed}")
        return v


class ScoreBreakdown(BaseModel):
    purpose_score: float = 0.0
    income_score: float = 0.0
    project_cost_score: float = 0.0
    location_score: float = 0.0


class RepaymentRuleResponse(BaseModel):
    id: str
    repayment_frequency: Optional[str] = None
    max_repayment_period: Optional[str] = None
    moratorium_period: Optional[str] = None
    condition: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ChannelPartnerResponse(BaseModel):
    id: str
    name: str
    partner_type: Optional[str] = None
    state_id: str
    district_id: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class SchemeListItemResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    category: Optional[str] = None
    purpose: Optional[str] = None
    description: Optional[str] = None
    min_project_cost: Optional[float] = None
    max_project_cost: Optional[float] = None
    finance_percentage: Optional[float] = None
    max_loan_amount: Optional[float] = None
    nsfdc_interest_rate: Optional[float] = None
    beneficiary_interest_rate: Optional[float] = None
    source_url: Optional[str] = None
    suitability_score: Optional[float] = None
    suitability_label: Optional[str] = None
    recommendation_reason: Optional[str] = None
    score_breakdown: Optional[ScoreBreakdown] = None

    model_config = ConfigDict(from_attributes=True)


class SchemeDetailResponse(SchemeListItemResponse):
    repayment_rules: List[RepaymentRuleResponse] = []
    # channel_partners: List[ChannelPartnerResponse] = []


class EMICalculatorRequest(BaseModel):
    loan_amount: float
    interest_rate: Optional[float] = None
    tenure_months: int
    moratorium_months: Optional[int] = None
    scheme_id: Optional[str] = None


class EMIScheduleBreakdown(BaseModel):
    month: int
    beginning_balance: float
    emi: float
    principal_paid: float
    interest_paid: float
    ending_balance: float


class EMICalculatorResponse(BaseModel):
    loan_amount: float
    annual_interest_rate: float
    tenure_months: int
    moratorium_months: int
    monthly_emi: float
    total_interest_payable: float
    total_payment: float
    schedule: List[EMIScheduleBreakdown] = []



