from typing import Optional
from fastapi import HTTPException, Request, status as http_status
from sqlalchemy.orm import Session
from app.core.exception import ServerException
from app.core.logger import get_logger
from app.core.message import ErrorMessage, SuccessMessage
from app.core.response import success_response
from app.repository.public_repository import (
    CountryRepository,
    StateRepository,
    DistrictRepository,
    SchemeRepository,
    ChannelPartnerRepository,
)
from app.schema.public import (
    CountryResponse,
    StateResponse,
    DistrictResponse,
    SchemeEligibilityRequest,
    SchemeListItemResponse,
    SchemeDetailResponse,
    RepaymentRuleResponse,
    ChannelPartnerResponse,
    EMICalculatorRequest,
    EMICalculatorResponse,
    EMIScheduleBreakdown,
)


logger = get_logger(__name__)

class PublicService:
    def __init__(self, request: Request, db: Session):
        self.request = request
        self.db = db
        self.country_repo = CountryRepository(db)
        self.state_repo = StateRepository(db)
        self.district_repo = DistrictRepository(db)
        self.scheme_repo = SchemeRepository(db)
        self.channel_partner_repo = ChannelPartnerRepository(db)

    # Method: Get Countries
    def list_countries(self):
        try:
            result = self.country_repo.get_all(limit=1000)

            # Now we need to Make Serializable DB Objects 
            countries = []
            for db_obj in result:
                countries.append(CountryResponse.model_validate(db_obj).model_dump())

            return success_response(
                status_code = http_status.HTTP_200_OK,
                msg = SuccessMessage.COUNTRIES_FETCHED_SUCCESSFULLY,
                data = countries
            )
        except HTTPException:
            raise 
        except Exception as e:
            raise ServerException(str(e))

    # Method: Get States
    def list_states(self, country_id: Optional[str] = None):
        try:
            if not country_id:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.COUNTRY_ID_REQUIRED,
                )

            result = self.state_repo.get_all(limit=1000, filters={"country_id": country_id})

            states = []
            for db_obj in result:
                states.append(StateResponse.model_validate(db_obj).model_dump())

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.STATES_FETCHED_SUCCESSFULLY,
                data=states,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: Get Districts
    def list_districts(self, state_id: Optional[str] = None):
        try:
            if not state_id:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.STATE_ID_REQUIRED,
                )

            result = self.district_repo.get_all(limit=1000, filters={"state_id": state_id})

            districts = []
            for db_obj in result:
                districts.append(DistrictResponse.model_validate(db_obj).model_dump())

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.DISTRICTS_FETCHED_SUCCESSFULLY,
                data=districts,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: List All Schemes
    def list_schemes(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ):
        try:
            schemes = self.scheme_repo.get_all_schemes(
                skip=skip,
                limit=limit,
                category=category,
                search=search,
            )
            results = [
                SchemeListItemResponse.model_validate(scheme).model_dump()
                for scheme in schemes
            ]
            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.SCHEMES_FETCHED_SUCCESSFULLY,
                data=results,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: Get Eligible Schemes
    def get_eligible_schemes(self, payload: SchemeEligibilityRequest):
        try:
            from app.services.ai_eligibility_engine import AIEligibilityEngine

            schemes = self.scheme_repo.get_eligible_schemes(
                project_cost=payload.project_cost,
                annual_income=payload.annual_income,
                category=payload.category,
                purpose=payload.purpose,
                state_id=payload.state_id,
                district_id=payload.district_id,
            )

            results = []
            for scheme in schemes:
                has_location = bool(payload.state_id or payload.district_id)
                evaluation = AIEligibilityEngine.evaluate_scheme(
                    scheme=scheme,
                    user_request=payload,
                    has_location_match=has_location,
                )

                if not evaluation["is_eligible"]:
                    continue

                item_data = SchemeListItemResponse.model_validate(scheme).model_dump()
                item_data.update({
                    "suitability_score": evaluation["suitability_score"],
                    "suitability_label": evaluation["suitability_label"],
                    "recommendation_reason": evaluation["recommendation_reason"],
                    "score_breakdown": evaluation["score_breakdown"].model_dump(),
                })
                results.append(item_data)

            # Rank schemes descending by suitability score
            results.sort(key=lambda x: x["suitability_score"] or 0.0, reverse=True)

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.SCHEMES_FETCHED_SUCCESSFULLY,
                data=results,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: Get Scheme Details with Repayment Rules and Area Channel Partners
    def get_scheme_details(
        self,
        scheme_id: str,
        state_id: Optional[str] = None,
        district_id: Optional[str] = None,
    ):
        try:
            scheme = self.scheme_repo.get(scheme_id)
            if not scheme:
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessage.SCHEME_NOT_FOUND,
                )

            # Extract base scheme info
            base_info = SchemeListItemResponse.model_validate(scheme).model_dump()

            # Format repayment rules
            repayment_rules = [
                RepaymentRuleResponse.model_validate(rule).model_dump()
                for rule in scheme.repayment_rules
            ]

            # Format channel partners (with optional location filtering)
            channel_partners = []
            for scp in scheme.scheme_channel_partners:
                cp = scp.channel_partner
                if not cp:
                    continue
                if state_id and cp.state_id != state_id:
                    continue
                if district_id and cp.district_id != district_id:
                    continue
                channel_partners.append(ChannelPartnerResponse.model_validate(cp).model_dump())

            response_data = SchemeDetailResponse(
                **base_info,
                repayment_rules=repayment_rules,
                # channel_partners=channel_partners,
            ).model_dump()

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.SCHEME_DETAILS_FETCHED_SUCCESSFULLY,
                data=response_data,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: Calculate Scheme EMI
    def calculate_emi(self, payload: EMICalculatorRequest):
        try:
            loan_amount = payload.loan_amount
            if loan_amount <= 0:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.INVALID_LOAN_AMOUNT,
                )

            tenure_months = payload.tenure_months
            if tenure_months <= 0:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.INVALID_TENURE,
                )

            annual_interest_rate = payload.interest_rate
            moratorium_months = payload.moratorium_months
            target_scheme = None

            if payload.scheme_id:
                target_scheme = self.scheme_repo.get(payload.scheme_id)
                if not target_scheme and (annual_interest_rate is None or moratorium_months is None):
                    raise HTTPException(
                        status_code=http_status.HTTP_404_NOT_FOUND,
                        detail=ErrorMessage.SCHEME_NOT_FOUND,
                    )

            # If interest_rate is not provided, try fetching from scheme
            if annual_interest_rate is None and target_scheme:
                if target_scheme.beneficiary_interest_rate is not None:
                    annual_interest_rate = float(target_scheme.beneficiary_interest_rate)
                elif target_scheme.nsfdc_interest_rate is not None:
                    annual_interest_rate = float(target_scheme.nsfdc_interest_rate)

            if annual_interest_rate is None or annual_interest_rate < 0:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.INTEREST_RATE_REQUIRED,
                )

            # Extract max tenure and moratorium_months from scheme repayment rules if scheme_id is provided
            max_tenure_months = None
            if moratorium_months is None:
                moratorium_months = 0

            if target_scheme and target_scheme.repayment_rules:
                import re
                for rule in target_scheme.repayment_rules:
                    if max_tenure_months is None and rule.max_repayment_period:
                        rule_str = str(rule.max_repayment_period).lower()
                        match = re.search(r"(\d+)\s*(year|month)?", rule_str)
                        if match:
                            num = int(match.group(1))
                            unit = match.group(2)
                            if unit and "year" in unit:
                                max_tenure_months = num * 12
                            else:
                                max_tenure_months = num

                    if payload.moratorium_months is None and rule.moratorium_period:
                        match = re.search(r"\d+", str(rule.moratorium_period))
                        if match:
                            moratorium_months = int(match.group(0))

            if max_tenure_months is not None and tenure_months > max_tenure_months:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=f"Tenure cannot exceed maximum repayment period of {max_tenure_months} months for this scheme",
                )

            if moratorium_months >= tenure_months:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail="Moratorium period cannot be equal to or greater than loan tenure",
                )

            repayment_tenure = tenure_months - moratorium_months

            # EMI Calculation for active repayment period
            if annual_interest_rate == 0:
                monthly_emi = round(loan_amount / repayment_tenure, 2)
                monthly_rate = 0.0
            else:
                monthly_rate = (annual_interest_rate / 100) / 12
                emi_val = (
                    loan_amount
                    * monthly_rate
                    * ((1 + monthly_rate) ** repayment_tenure)
                    / (((1 + monthly_rate) ** repayment_tenure) - 1)
                )
                monthly_emi = round(emi_val, 2)

            # Build monthly schedule
            schedule = []
            balance = float(loan_amount)
            total_payment = 0.0

            for m in range(1, tenure_months + 1):
                if m <= moratorium_months:
                    interest_paid = round(balance * monthly_rate, 2)
                    principal_paid = 0.0
                    current_emi = interest_paid
                    ending_balance = balance
                else:
                    interest_paid = round(balance * monthly_rate, 2)
                    if m == tenure_months:
                        principal_paid = balance
                        current_emi = round(principal_paid + interest_paid, 2)
                    else:
                        principal_paid = round(monthly_emi - interest_paid, 2)
                        current_emi = monthly_emi

                    ending_balance = max(0.0, round(balance - principal_paid, 2))

                schedule.append(
                    EMIScheduleBreakdown(
                        month=m,
                        beginning_balance=balance,
                        emi=current_emi,
                        principal_paid=principal_paid,
                        interest_paid=interest_paid,
                        ending_balance=ending_balance,
                    )
                )
                total_payment += current_emi
                balance = ending_balance

            total_payment = round(total_payment, 2)
            total_interest_payable = round(total_payment - loan_amount, 2)

            response_data = EMICalculatorResponse(
                loan_amount=loan_amount,
                annual_interest_rate=annual_interest_rate,
                tenure_months=tenure_months,
                moratorium_months=moratorium_months,
                monthly_emi=monthly_emi,
                total_interest_payable=total_interest_payable,
                total_payment=total_payment,
                schedule=schedule,
            ).model_dump()

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.EMI_CALCULATED_SUCCESSFULLY,
                data=response_data,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))

    # Method: List Channel Partners by scheme_id, country_id, state_id, district_id
    def list_channel_partners(
        self,
        country_id: Optional[str] = None,
        state_id: Optional[str] = None,
        district_id: Optional[str] = None,
        scheme_id: Optional[str] = None,
    ):
        try:
            db_channel_partners = self.channel_partner_repo.get_channel_partners(
                country_id=country_id,
                state_id=state_id,
                district_id=district_id,
                scheme_id=scheme_id,
            )

            result = [
                ChannelPartnerResponse.model_validate(cp).model_dump()
                for cp in db_channel_partners
            ]

            return success_response(
                status_code=http_status.HTTP_200_OK,
                msg=SuccessMessage.CHANNEL_PARTNERS_FETCHED_SUCCESSFULLY,
                data=result,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise ServerException(str(e))





    
    