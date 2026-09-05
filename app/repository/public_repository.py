from typing import Optional, List
from sqlalchemy.orm import Session
from app.repository.base_repository import BaseRepository
from app.db.models.country import Country
from app.db.models.state import State
from app.db.models.district import District
from app.db.models.scheme import Scheme
from app.db.models.scheme_repayment_rule import SchemeRepaymentRule
from app.db.models.channel_partner import ChannelPartner
from app.db.models.scheme_channel_partner import SchemeChannelPartner


# Country Repository 
class CountryRepository(BaseRepository[Country]):
    def __init__(self, db: Session):
        super().__init__(Country, db)

# State Repository 
class StateRepository(BaseRepository[State]):
    def __init__(self, db: Session):
        super().__init__(State, db)

# District Repository 
class DistrictRepository(BaseRepository[District]):
    def __init__(self, db: Session):
        super().__init__(District, db)

# Scheme Repository
class SchemeRepository(BaseRepository[Scheme]):
    def __init__(self, db: Session):
        super().__init__(Scheme, db)

    def get_eligible_schemes(
        self,
        project_cost: Optional[float] = None,
        category: Optional[str] = None,
        state_id: Optional[str] = None,
        district_id: Optional[str] = None,
    ) -> List[Scheme]:
        query = self.db.query(Scheme).filter(
            Scheme.is_active == True,
            Scheme.is_deleted == False,
        )

        if project_cost is not None:
            query = query.filter(
                (Scheme.min_project_cost == None) | (Scheme.min_project_cost <= project_cost),
                (Scheme.max_project_cost == None) | (Scheme.max_project_cost >= project_cost),
            )

        if category:
            query = query.filter(Scheme.category.ilike(f"%{category}%"))

        if state_id or district_id:
            query = query.join(Scheme.scheme_channel_partners).join(SchemeChannelPartner.channel_partner)
            if state_id:
                query = query.filter(ChannelPartner.state_id == state_id)
            if district_id:
                query = query.filter(ChannelPartner.district_id == district_id)
            query = query.distinct()

        return query.all()

# SchemeRepaymentRule Repository
class SchemeRepaymentRuleRepository(BaseRepository[SchemeRepaymentRule]):
    def __init__(self, db: Session):
        super().__init__(SchemeRepaymentRule, db)

# ChannelPartner Repository
class ChannelPartnerRepository(BaseRepository[ChannelPartner]):
    def __init__(self, db: Session):
        super().__init__(ChannelPartner, db)

# SchemeChannelPartner Repository
class SchemeChannelPartnerRepository(BaseRepository[SchemeChannelPartner]):
    def __init__(self, db: Session):
        super().__init__(SchemeChannelPartner, db)

