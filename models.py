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


tenant_user_association = Table(
    'tenant_user_association',
    Base.metadata,
    Column('tenant_guid', String, ForeignKey('tenant.guid')),
    Column('user_guid', String, ForeignKey('user.guid'))
)

group_user_association = Table(
    'group_user_association',
    Base.metadata,
    Column('group_guid', String, ForeignKey('group.guid')),
    Column('user_guid', String, ForeignKey('user.guid'))
)


group_permission_association = Table(
    'group_permission_association',
    Base.metadata,
    Column('group_guid', String, ForeignKey('group.guid')),
    Column('permision_id', Integer, ForeignKey('permission.id'))
)

class BillingType(Base):
    __tablename__ = 'billing_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    billing_type_name =  Column(String(128), unique=True)
    subscription = relationship('Subscription', back_populates='billing_type')

class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(128), unique=True)
    groups = relationship('Group', secondary=group_permission_association, back_populates='permissions')


class Group(Base):
    __tablename__ = 'group'

    guid = Column(String, index=True, primary_key=True, nullable=False)
    # tenant = 
    name = Column(String(50), unique=True)
    buc_code = Column(String(128))
    permissions = relationship('Permission', secondary=group_permission_association, back_populates='groups')
    members = relationship('User', secondary=group_user_association, back_populates='groups')


class Subscription(Base):
    __tablename__ = 'subscription'

    guid = Column(String, index=True, primary_key=True, nullable=False)
    name = Column(String(128))
    # valiidity 
    billing_type_id = Column(Integer, ForeignKey('billing_type.id',ondelete='CASCADE'), nullable=True)
    billing_type = relationship('BillingType', back_populates='subscription')
    # modules = 
    user_upper_limit = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    pros_and_cons = Column(String(255), nullable=True)
    
class Tenant(Base):
    __tablename__ = 'tenant'

    guid = Column(String, index=True, primary_key=True, nullable=False)
    name = Column(String(50), unique=True)
    vendor_code = Column(String(128))
    pan_no = Column(String(128))
    gst_no = Column(String(128))
    cin_no = Column(String(128))
    iso_no = Column(String(128))
    email = Column(String(128))
    phone_no = Column(String(128))
    address = Column(String(128))
    website = Column(String(128))
    subscription= Column(String(128))
    users = relationship('User', secondary=tenant_user_association, back_populates='tenant')

class User(Base):
    __tablename__ = "user"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(256), nullable=False)
    tenant = relationship('Tenant', secondary=tenant_user_association, back_populates='users')
    groups = relationship('Group', secondary=group_user_association, back_populates='members')


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
    batch_num = Column(String(255), nullable=True)
    stock_batch_description = Column(String(128), nullable=True)
    stock_qty = Column(Integer, nullable=True)
    stock_unit_price = Column(Float, nullable=True)
    stock_date_of_purchase = Column(Date, nullable=True)

    consignment = relationship("InvoiceConsignment", back_populates="stockbatchinfo")
#make one to many with stock detail

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

consignment_item_association = Table(
    'consignment_item_association',
    Base.metadata,
    Column('consignment_guid', String, ForeignKey('consignment.guid')),
    Column('item_guid', String, ForeignKey('item.guid'))
)

class Product(Base):
    __tablename__ = "product"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    description = Column(String(128), nullable=True)
    vendor = Column(String(128), nullable=True)
    batch_id = Column(String(128), nullable=True)
    cost_price = Column(Float, nullable=True)
    item = relationship("Item", back_populates="product")
    # purchase_date  = Column(Date, nullable=True)
    

class Item(Base):
    __tablename__ = 'item'

    guid = Column(String, index=True, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_guid = Column(String, ForeignKey('product.guid',ondelete='CASCADE'), nullable=True)
    product = relationship("Product", back_populates="item")

    consignment = relationship('InvoiceConsignment', secondary=consignment_item_association, back_populates='items')


class InvoiceConsignment(Base):
    __tablename__ = "consignment"

    guid = Column(String, index=True, primary_key=True, nullable=False)
    reverse_charge = Column(Boolean, nullable=True)
    is_cancelled = Column(Boolean, nullable=True)
    cancellation_reason  = Column(String(128), nullable=True)
    date = Column(DateTime,default=datetime.utcnow() )
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
    po_date  = Column(Date, nullable=True)
    place_of_supply  = Column(String(128), nullable=True)
    lr_no  = Column(String(128), nullable=True)
    lr_date = Column(Date, nullable=True)
    transporter_name  = Column(String(128), nullable=True)
    preparation_date = Column(Date, nullable=True)
    issue_date = Column(Date, nullable=True)
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
    items = relationship('Item', secondary=consignment_item_association, back_populates='consignment')