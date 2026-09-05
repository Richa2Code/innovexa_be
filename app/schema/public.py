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