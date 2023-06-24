from pydantic import BaseModel

class InvoiceCreate(BaseModel):
    product: str

class InvoiceDelete(BaseModel):
    id: int

class Invoice(InvoiceCreate):

    class Config:
        orm_mode = True

class BankDetailCreateView(BaseModel):
    guid : str
    account_company_name: str
    account_fname : str
    account_lname :str
    bank_ifsc_code : str
    bank_address : str 
    bank_country : str
    bank_country : str
    bank_phone_number :str
    bank_email :str

    class Config:
        orm_mode = True

class BankDetailCreate(BaseModel):
    account_company_name: str
    account_fname : str
    account_lname :str
    bank_ifsc_code : str
    bank_address : str 
    bank_country : str
    bank_country : str
    bank_phone_number :str
    bank_email :str

    class Config:
        orm_mode = True

class BankDetailUpdate(BaseModel):
    account_fname : str
    account_lname :str
    bank_ifsc_code : str
    bank_address : str 
    bank_country : str
    bank_country : str
    bank_phone_number :str
    bank_email :str

    class Config:
        orm_mode = True