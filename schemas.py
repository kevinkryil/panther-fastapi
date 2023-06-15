from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    product: str

class InvoiceDelete(BaseModel):
    id: int

class Invoice(InvoiceCreate):

    class Config:
        orm_mode = True
