from typing import Optional
from fastapi import APIRouter, Request, Depends, Query, status as http_status
from app.db.session import get_db
from app.schema.public import SchemeEligibilityRequest, EMICalculatorRequest
from app.services.public_service import PublicService

router = APIRouter(
    prefix="/public"
)

@router.get("/countries")
def list_country(request: Request, db = Depends(get_db)):
    service = PublicService(request, db)
    return service.list_countries()


@router.get("/states")
def list_states(request: Request, country_id: Optional[str] = Query(None), db = Depends(get_db)):
    service = PublicService(request, db)
    return service.list_states(country_id=country_id)


@router.get("/districts")
def list_districts(request: Request, state_id: Optional[str] = Query(None), db = Depends(get_db)):
    service = PublicService(request, db)
    return service.list_districts(state_id=state_id)


@router.get("/schemes")
def list_schemes(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db = Depends(get_db),
):
    service = PublicService(request, db)
    return service.list_schemes(skip=skip, limit=limit, category=category, search=search)


@router.post("/schemes/eligible")
def get_eligible_schemes(
    request: Request,
    payload: SchemeEligibilityRequest,
    db = Depends(get_db),
):
    service = PublicService(request, db)
    return service.get_eligible_schemes(payload)


@router.get("/schemes/{scheme_id}")
def get_scheme_details(
    request: Request,
    scheme_id: str,
    state_id: Optional[str] = Query(None),
    district_id: Optional[str] = Query(None),
    db = Depends(get_db),
):
    service = PublicService(request, db)
    return service.get_scheme_details(scheme_id=scheme_id, state_id=state_id, district_id=district_id)


@router.post("/schemes/emi-calculator")
def calculate_scheme_emi(
    request: Request,
    payload: EMICalculatorRequest,
    db = Depends(get_db),
):
    service = PublicService(request, db)
    return service.calculate_emi(payload)


@router.get("/channel-partners")
def list_channel_partners(
    request: Request,
    country_id: Optional[str] = Query(None),
    state_id: Optional[str] = Query(None),
    district_id: Optional[str] = Query(None),
    scheme_id: Optional[str] = Query(None),
    db = Depends(get_db),
):
    service = PublicService(request, db)
    return service.list_channel_partners(
        country_id=country_id,
        state_id=state_id,
        district_id=district_id,
        scheme_id=scheme_id,
    )


