from pydantic import BaseModel


class CountrySchem(BaseModel):
    id: int
    name: str
    organization_id: int