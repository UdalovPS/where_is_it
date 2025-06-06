from pydantic import BaseModel


class SimilarItemsSchem(BaseModel):
    id: int
    name: str
    similarity_score: float

    class Config:
        from_attributes = True