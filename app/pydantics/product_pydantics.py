from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    total_quantity: int = Field(..., gt=0)

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    name: str
    total_quantity: int
    created_by: int

    class Config:
        orm_mode = True
