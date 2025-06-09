from pydantic import BaseModel


class SimilarItemsSchem(BaseModel):
    id: int
    name: str
    similarity_score: float
    category: str

    class Config:
        from_attributes = True