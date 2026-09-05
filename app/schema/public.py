from typing import Optional, List
from pydantic import BaseModel, ConfigDict

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
    project_cost: Optional[float] = None
    category: Optional[str] = None
    state_id: Optional[str] = None
    district_id: Optional[str] = None


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

    model_config = ConfigDict(from_attributes=True)


class SchemeDetailResponse(SchemeListItemResponse):
    repayment_rules: List[RepaymentRuleResponse] = []
    channel_partners: List[ChannelPartnerResponse] = []
