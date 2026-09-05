from typing import Optional
from fastapi import HTTPException, Request, status as http_status
from sqlalchemy.orm import Session
from app.core.exception import ServerException
from app.core.logger import get_logger
from app.core.message import ErrorMessage, SuccessMessage
from app.core.response import success_response
from app.repository.public_repository import CountryRepository, StateRepository, DistrictRepository
from app.schema.public import CountryResponse, StateResponse, DistrictResponse

logger = get_logger(__name__)

class PublicService:
    def __init__(self, request: Request, db: Session):
        self.request = request
        self.db = db
        self.country_repo = CountryRepository(db)
        self.state_repo = StateRepository(db)
        self.district_repo = DistrictRepository(db)

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

    
    