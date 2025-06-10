from pydantic import BaseModel

from schemas.storage_schem import districts_schem


class CitySchem(BaseModel):
    id: int
    name: str
    organization_id: int
    district_data: districts_schem.DistrictSchem