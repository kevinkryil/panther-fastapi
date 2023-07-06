from pydantic import BaseModel, EmailStr

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

# class ClientCreateView(BaseModel):
#     guid : str
#     client_company_name : str
#     client_contact_name : str
#     client_contact_designation : str
#     client_city : str
#     client_state : str
#     client_pincode : str
#     client_country : str
#     client_phone_no : str
#     client_email : str
#     client_state_code : str
#     client_gstin : str

#     class Config:
#         orm_mode = True

class ClientCreate(BaseModel):
    client_company_name : str
    client_contact_name : str
    client_contact_designation : str
    client_city : str
    client_state : str
    client_pincode : str
    client_country : str
    client_phone_no : str
    client_email : str
    client_state_code : str
    client_gstin : str

    class Config:
        orm_mode = True

class StockDetailCreate(BaseModel):
    stock_name : str

    class Config:
        orm_mode = True
    
class StockBatchInfoCreate(BaseModel):
    stock_batch_description : str
    stock_qty : int
    stock_unit_price : float
    # stock_date_of_purchase : 
    class Config:
        orm_mode = True

class ItemDetailCreate(BaseModel):
    invoice_item_qty : int
    invoice_item_taxable_value : float
    invoice_item_tag_no : str
    invoice_item_currency : str
    class Config:
        orm_mode = True

class TermsAndConditionsCreate(BaseModel):
    tac_description : str
    class Config:
        orm_mode = True

class SignatoryCreate(BaseModel):
    signatory_name : str
    signatory_img_b64 : str
    class Config:
        orm_mode = True

class TaxationCreate(BaseModel):
    policy_no : str
    freight_terms : str
    tax_component_1 : str
    tax_component_2 : str
    tax_component_3 : str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : str
    password : str
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    guid : str
    email : str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    guid : str
    email : str  
    class Config:
        orm_mode = True