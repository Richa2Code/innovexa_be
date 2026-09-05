from app.repository.base_repository import BaseRepository
from app.db.models.country import Country
from app.db.models.state import State
from app.db.models.district import District
from sqlalchemy.orm import Session


# Country Repositorty 
class CountryRepository(BaseRepository[Country]):
    def __init__(self, db: Session):
        super().__init__(Country, db)

# State Repositorty 
class StateRepository(BaseRepository[State]):
    def __init__(self, db: Session):
        super().__init__(State, db)

# District Repositorty 
class DistrictRepository(BaseRepository[District]):
    def __init__(self, db: Session):
        super().__init__(District, db)
