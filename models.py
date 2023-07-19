from datetime import datetime
from random import random
import string
import uuid
from pydantic import Field
import shortuuid
from sqlalchemy import DateTime, Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Table, func, Date
from sqlalchemy.orm import relationship
from database import Base
from utils import *

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

tenant_user_association = Table(
    'tenant_user_association',
    Base.metadata,
    Column('tenant_id', Integer, ForeignKey('tenant.id')),
    Column('user_guid', String, ForeignKey('user.guid'))
)

class Tenant(Base):
    __tablename__ = 'tenant'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    users = relationship('User', secondary=tenant_user_association, back_populates='tenant')


class User(Base):
    __tablename__ = "user"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)
    tenant = relationship('Tenant', secondary=tenant_user_association, back_populates='users')


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

    guid = Column(String, index=True, primary_key=True, nullable=False)
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

    guid = Column(String, index=True, primary_key=True, nullable=False)
    stock_name = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="stockdetail")

class StockBatchInfo(Base):
    __tablename__ = "stockbatchinfo"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    stock_batch_description = Column(String(128), nullable=True)
    stock_qty = Column(Integer, nullable=True)
    stock_unit_price = Column(Float, nullable=True)
    stock_date_of_purchase = Column(Date, nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="stockbatchinfo")

class ItemDetail(Base):
    __tablename__ = "itemdetail"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    invoice_item_qty = Column(Integer, nullable=True)
    invoice_item_taxable_value = Column(Float, nullable=True)
    invoice_item_tag_no  = Column(String(128), nullable=True)
    invoice_item_currency  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="itemdetail")

class TermsAndConditions(Base):
    __tablename__ = "termsandconditions"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    tac_description  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="tnc")

class Signatory(Base):
    __tablename__ = "signatory"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    signatory_name  = Column(String(128), nullable=True)
    signatory_img_b64  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="signatory")

class Taxation(Base):
    __tablename__ = "taxation"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    policy_no  = Column(String(128), nullable=True)
    freight_terms  = Column(String(128), nullable=True)
    tax_component_1  = Column(String(128), nullable=True)
    tax_component_2  = Column(String(128), nullable=True)
    tax_component_3  = Column(String(128), nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="taxation")

consignment_product_association = Table(
    'consignment_product_association',
    Base.metadata,
    Column('consignment_guid', String, ForeignKey('consignment.guid')),
    Column('product_guid', String, ForeignKey('product.guid'))
)

class Product(Base):
    __tablename__ = "product"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    description = Column(String(128), nullable=True)
    vendor = Column(String(128), nullable=True)
    batch_id = Column(String(128), nullable=True)
    cost_price = Column(Float, nullable=True)
    purchase_date  = Column(Date, nullable=True)

    consignment = relationship('InvoiceConsignment', secondary=consignment_product_association, back_populates='product')

    # consignment1 = relationship("InvoiceConsignment", back_populates="product1")
    # consignment2 = relationship("InvoiceConsignment", back_populates="product2")
    # consignment3 = relationship("InvoiceConsignment", back_populates="product3")
    # consignment4 = relationship("InvoiceConsignment", back_populates="product4")
    # consignment5 = relationship("InvoiceConsignment", back_populates="product5")
    # consignment6 = relationship("InvoiceConsignment", back_populates="product6")

class InvoiceConsignment(Base):
    __tablename__ = "consignment"

    guid = Column(String, index=True, primary_key=True, nullable=False)
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
    product = relationship('Product', secondary=consignment_product_association, back_populates='consignment')
    
    # product1_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product1 = relationship("Product", back_populates='consignment1')
    # product1qty = Column(Float, nullable=True)
    # product2_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product2 = relationship("Product", back_populates='consignment2')
    # product2qty = Column(Float, nullable=True)
    # product3_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product3 = relationship("Product", back_populates='consignment3')
    # product3qty = Column(Float, nullable=True)
    # product4_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product4 = relationship("Product", back_populates='consignment4')
    # product4qty = Column(Float, nullable=True)
    # product5_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product5 = relationship("Product", back_populates='consignment5')
    # product5qty = Column(Float, nullable=True)
    # product6_guid = Column(String, ForeignKey('product.guid', ondelete="CASCADE"), nullable=True)
    # product6 = relationship("Product", back_populates='consignment6')
    # product6qty = Column(Float, nullable=True)
    bank_detail_guid = Column(String, ForeignKey('bankdetail.guid',ondelete='CASCADE'), nullable=True)
    bankdetail = relationship("BankDetail", back_populates='consignment')
    client_guid = Column(String, ForeignKey('client.guid', ondelete="CASCADE"), nullable=True)
    client = relationship("Client", back_populates='consignment')
    stockdetail_guid = Column(String, ForeignKey('stockdetail.guid', ondelete="CASCADE"), nullable=True)
    stockdetail = relationship("StockDetail", back_populates='consignment')
    stockbatchinfo_guid = Column(String, ForeignKey('stockbatchinfo.guid', ondelete="CASCADE"), nullable=True)
    stockbatchinfo = relationship("StockBatchInfo", back_populates='consignment')
    itemdetail_guid = Column(String, ForeignKey('itemdetail.guid', ondelete="CASCADE"), nullable=True)
    itemdetail = relationship("ItemDetail", back_populates='consignment')
    tnc_guid = Column(String, ForeignKey('termsandconditions.guid', ondelete="CASCADE"), nullable=True)
    tnc = relationship("TermsAndConditions", back_populates='consignment')
    signatory_guid = Column(String, ForeignKey('signatory.guid', ondelete="CASCADE"), nullable=True)
    signatory = relationship("Signatory", back_populates='consignment')
    taxation_guid = Column(String, ForeignKey('taxation.guid', ondelete="CASCADE"), nullable=True)
    taxation = relationship("Taxation", back_populates='consignment')

