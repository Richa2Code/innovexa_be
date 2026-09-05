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

    # Method: Get Eligible Schemes
    def get_eligible_schemes(self, payload: SchemeEligibilityRequest):
        try:
            schemes = self.scheme_repo.get_eligible_schemes(
                project_cost=payload.project_cost,
                category=payload.category,
                state_id=payload.state_id,
                district_id=payload.district_id,
            )

            results = []
            for scheme in schemes:
                results.append(SchemeListItemResponse.model_validate(scheme).model_dump())

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
                channel_partners=channel_partners,
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


    
    