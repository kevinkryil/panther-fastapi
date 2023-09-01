from typing import List
from pydantic import BaseModel, EmailStr
from datetime import date, datetime

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
    batch_num : str
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

class ProductCreate(BaseModel):
    description : str 
    vendor : str
    batch_id :  str
    cost_price : float
    # purchase_date : 
    class Config:
        orm_mode = True

class ProductOut(ProductCreate):
    guid : str
    class Config:
        orm_mode = True

class ConsignmentCreate(BaseModel):
    guid : str
    reverse_charge : bool
    is_cancelled : bool
    cancellation_reason : str
    state : str
    state_code : str
    country : str
    destination :str
    rfq_item_no : str
    rfq_item_name : str
    goods_name : str
    hsn_no : str
    eway_no : str
    po_no : str
    po_date : date
    place_of_supply : str
    lr_no : str
    lr_date : date
    transporter_name : str
    preparation_date : date
    issue_date : date
    bank_detail_guid : str
    client_guid : str 
    stockdetail_guid : str
    stockbatchinfo_guid : str
    itemdetail_guid : str
    tnc_guid : str
    signatory_guid : str
    taxation_guid : str
    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    quantity : int
    product_guid : str
    class Config:
        orm_mode = True

class ItemOut(ItemCreate):
    guid : str
    class Config:
        orm_mode = True

class Items(BaseModel):
    product : ProductOut
    quantity : int
    class Config:
        orm_mode = True

class ConsignmentOut(BaseModel):
    guid : str
    reverse_charge : bool
    is_cancelled : bool
    cancellation_reason : str
    date : datetime
    state : str
    state_code : str
    country : str
    destination :str
    rfq_item_no : str
    rfq_item_name : str
    goods_name : str
    hsn_no : str
    eway_no : str
    po_no : str
    po_date : date
    place_of_supply : str
    lr_no : str
    lr_date : date
    transporter_name : str
    preparation_date : date
    issue_date  : date
    bank_detail_guid : str
    client_guid : str 
    stockdetail_guid : str
    stockbatchinfo_guid : str
    itemdetail_guid : str
    tnc_guid : str
    signatory_guid : str
    taxation_guid : str
    items : List[Items] 
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email : str
    password : str
    tenant : str
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    guid : str
    email : str
    # tenant : str
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

class TenantCreate(BaseModel):
    name : str
    vendor_code : str
    pan_no : str
    gst_no : str
    cin_no : str
    iso_no : str
    email : str
    phone_no : str
    address : str
    website : str
    subscription : str
    class Config:
        orm_mode = True

class TenantOut(TenantCreate):
    guid : str
    class Config:
        orm_mode = True

class GroupCreate(BaseModel):
    name : str
    buc_code : str
    class Config:
        orm_mode = True


class GroupOut(GroupCreate):
    guid : str
    class Config:
        orm_mode = True

class SubscriptionCreate(BaseModel):
    name : str
    user_upper_limit : int
    description : str
    pros_and_cons : str
    class Config:
        orm_mode = True

class SubscriptionOut(SubscriptionCreate):
    guid : str
    class Config:
        orm_mode = True

class PermissionCreate(BaseModel):
    permission_name : str
    class Config:
        orm_mode = True

class PermissionOut(PermissionCreate):
    id : int
    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    quantity : int
    product_guid : str
    class Config:
        orm_mode = True

class ItemOut(ItemCreate):
    guid : str
    class Config:
        orm_mode = True

class PageInfo(BaseModel):
    total : int
    page_number : int
    previous_page : str
    next_page : str
    class Config:
        orm_mode = True

class ConsignmentOutPage(BaseModel):
    info : PageInfo
    data : List[ConsignmentOut]
    class Config:
        orm_mode = True
