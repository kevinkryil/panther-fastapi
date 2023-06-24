from datetime import datetime
from random import random
import string
import uuid
from pydantic import Field
import shortuuid
from sqlalchemy import DateTime, Boolean, Column, DateTime, ForeignKey, Integer, String, Float, func, Date
from sqlalchemy.orm import relationship
from database import Base

# class Invoice(Base):
#     __tablename__ = "invoice"

#     id = Column(Integer, primary_key=True, index=True)
#     product = Column(String(128), index=True)

def shortuuid_random():
    alphabet = string.ascii_lowercase + string.digits
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(length=8)

def guid_gen(word="TMP"):
    try:
        datetime_now = datetime.now()
        year = datetime_now.year
        month = datetime_now.month
        day = datetime_now.day
        wordshort_form = word[0:3].lower()
        uuid = wordshort_form+ str(year)+ str(month) + str(day)+shortuuid_random()
        return uuid
    
    except:
        return {'detail':'Error Found!'}

class BankDetail(Base):
    __tablename__ = "bankdetail"

    # id = Column(Integer, index=True, primary_key=True)
    guid = Column(String, index=True, primary_key=True, nullable=False)
    account_company_name = Column(String(128), nullable=True, unique=True)
    account_fname = Column(String(128), nullable=True)
    account_lname = Column(String(128), nullable=True)
    bank_ifsc_code = Column(String(128), nullable=True)
    bank_address = Column(String(128), nullable=True)
    bank_country = Column(String(128), nullable=True)
    bank_phone_number = Column(String(128), nullable=True)
    bank_email = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String(128), default="SYSTEM")
    consignment = relationship("InvoiceConsignment", back_populates="bankdetail")

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    client_company_name = Column(String(128), nullable=True)
    client_contact_name = Column(String(128), nullable=True)
    client_contact_designation = Column(String(128), nullable=True)
    client_city = Column(String(128), nullable=True)
    client_state = Column(String(128), nullable=True)
    client_pincode = Column(String(128), nullable=True)
    client_country = Column(String(128), nullable=True)
    client_phone_no = Column(String(128), nullable=True)
    client_email = Column(String(128), nullable=True)
    client_state_code = Column(String(128), nullable=True)
    client_gstin = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="client")

class StockDetail(Base):
    __tablename__ = "stockdetail"

    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="stockdetail")

class StockBatchInfo(Base):
    __tablename__ = "stockbatchinfo"

    id = Column(Integer, primary_key=True, index=True)
    stock_batch_description = Column(String(128), nullable=True)
    stock_qty = Column(Integer, nullable=True)
    stock_unit_price = Column(Float, nullable=True)
    stock_date_of_purchase = Column(Date, nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="stockbatchinfo")

class ItemDetail(Base):
    __tablename__ = "itemdetail"

    id = Column(Integer, primary_key=True, index=True)
    invoice_item_qty = Column(Integer, nullable=True)
    invoice_item_taxable_value = Column(Float, nullable=True)
    invoice_item_tag_no  = Column(String(128), nullable=True)
    invoice_item_currency  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="itemdetail")

class TermsAndConditions(Base):
    __tablename__ = "termsandconditions"

    id = Column(Integer, primary_key=True, index=True)
    tac_description  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="tnc")

class Signatory(Base):
    __tablename__ = "signatory"

    id = Column(Integer, primary_key=True, index=True)
    signatory_name  = Column(String(128), nullable=True)
    signatory_img_b64  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="signatory")

class Taxation(Base):
    __tablename__ = "taxation"

    id = Column(Integer, primary_key=True, index=True)
    policy_no  = Column(String(128), nullable=True)
    freight_terms  = Column(String(128), nullable=True)
    tax_component_1  = Column(String(128), nullable=True)
    tax_component_2  = Column(String(128), nullable=True)
    tax_component_3  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="taxation")

# class Product(Base):
#     __tablename__ = "product"

#     id = Column(Integer, primary_key=True, index=True)
#     description = Column(String(128), nullable=True)
#     vendor = Column(String(128), nullable=True)
#     batch_id = Column(String(128), nullable=True)
#     cost_price = Column(Float, nullable=True)
#     purchase_date  = Column(Date, nullable=True)

#     consignment = relationship("InvoiceConsignment", back_populates="product1")
#     consignment = relationship("InvoiceConsignment", back_populates="product2")
#     consignment = relationship("InvoiceConsignment", back_populates="product3")
#     consignment = relationship("InvoiceConsignment", back_populates="product4")
#     consignment = relationship("InvoiceConsignment", back_populates="product5")
#     consignment = relationship("InvoiceConsignment", back_populates="product6")

class InvoiceConsignment(Base):
    __tablename__ = "consignment"

    id = Column(Integer, primary_key=True, index=True)
    # client = Column(Integer, ForeignKey('client.id', ondelete="CASCADE"), nullable=False)
    # stock_detail = Column(Integer, ForeignKey('stockdetail.id', ondelete="CASCADE"), nullable=False)
    # stock_batch_info = Column(Integer, ForeignKey('stockbatchinfo.id', ondelete="CASCADE"), nullable=False)
    # item_details = Column(Integer, ForeignKey('itemdetail.id', ondelete="CASCADE"), nullable=False)
    # tnc = Column(Integer, ForeignKey('termsandconditions.id', ondelete="CASCADE"), nullable=False)
    # signatory = Column(Integer, ForeignKey('signatory.id', ondelete="CASCADE"), nullable=False)
    # taxation = Column(Integer, ForeignKey('taxation.id', ondelete="CASCADE"), nullable=False)
    reverse_charge = Column(Boolean, nullable=True)
    is_cancelled = Column(Boolean, nullable=True)
    cancellation_reason  = Column(String(128), nullable=True)
    date = Column(Date, nullable=True)
    state  = Column(String(128), nullable=True)
    state_code  = Column(String(128), nullable=True) 
    country  = Column(String(128), nullable=True)
    destination  = Column(String(128), nullable=True)
    rfq_item_no  = Column(String(128), nullable=True)
    rfq_item_name  = Column(String(128), nullable=True) 
    goods_name  = Column(String(128), nullable=True)
    hsn_no  = Column(String(128), nullable=True)
    eway_no  = Column(String(128), nullable=True)
    po_no  = Column(String(128), nullable=True)
    po_date  = Column(String(128), nullable=True)
    place_of_supply  = Column(String(128), nullable=True)
    lr_no  = Column(String(128), nullable=True)
    lr_date = Column(Date, nullable=True)
    transporter_name  = Column(String(128), nullable=True)
    preparation_date = Column(Date, nullable=True)
    issue_date = Column(Date, nullable=True)


    # product1 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=False)
    # product1qty = Column(Float, nullable=True)
    # product2 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    # product2qty = Column(Float, nullable=True)
    # product3 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    # product3qty = Column(Float, nullable=True)
    # product4 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    # product4qty = Column(Float, nullable=True)
    # product5 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    # product5qty = Column(Float, nullable=True)
    # product6 = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    # product6qty = Column(Float, nullable=True)

    bank_detail_id = Column(String, ForeignKey('bankdetail.guid',ondelete='CASCADE'), nullable=True)
    bankdetail = relationship("BankDetail", back_populates='consignment')
    client_id = Column(Integer, ForeignKey('client.id', ondelete="CASCADE"), nullable=True)
    client = relationship("Client", back_populates='consignment')
    stockdetail_id = Column(Integer, ForeignKey('stockdetail.id', ondelete="CASCADE"), nullable=True)
    stockdetail = relationship("StockDetail", back_populates='consignment')
    stockbatchinfo_id = Column(Integer, ForeignKey('stockbatchinfo.id', ondelete="CASCADE"), nullable=True)
    stockbatchinfo = relationship("StockBatchInfo", back_populates='consignment')
    itemdetail_id = Column(Integer, ForeignKey('itemdetail.id', ondelete="CASCADE"), nullable=True)
    itemdetail = relationship("ItemDetail", back_populates='consignment')
    tnc_id = Column(Integer, ForeignKey('termsandconditions.id', ondelete="CASCADE"), nullable=True)
    tnc = relationship("TermsAndConditions", back_populates='consignment')
    signatory_id = Column(Integer, ForeignKey('signatory.id', ondelete="CASCADE"), nullable=True)
    signatory = relationship("Signatory", back_populates='consignment')
    taxation_id = Column(Integer, ForeignKey('taxation.id', ondelete="CASCADE"), nullable=True)
    taxation = relationship("Taxation", back_populates='consignment')
    # product1 = relationship("Product", back_populates='consignment')
    # product2 = relationship("Product", back_populates='consignment')
    # product3 = relationship("Product", back_populates='consignment')
    # product4 = relationship("Product", back_populates='consignment')
    # product5 = relationship("Product", back_populates='consignment')
    # product6 = relationship("Product", back_populates='consignment')



    



