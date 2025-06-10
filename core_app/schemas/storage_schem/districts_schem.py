from pydantic import BaseModel

from schemas.storage_schem import countries_schem


class DistrictSchem(BaseModel):
    id: int
    name: str
    organization_id: int
    country_data: countries_schem.CountrySchem