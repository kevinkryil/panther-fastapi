from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from models import *
from utils import *
from oauth2 import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panther")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        return 'Error Found!'

##############################################################################
@app.post("/user/create", tags=['Auth'], response_model=schemas.UserOut)
def create_user(request : schemas.UserCreate,db: Session = Depends(get_db)):
    user = models.User(guid=guid_gen(), email=request.email, password=get_password_hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", tags=['Auth'], response_model=schemas.Token)
def login(request:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(User.email==request.username).first()
    if not user or  not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = create_access_token(data={"guid":user.guid, "email":user.email})
    return {"access_token":access_token, "token_type":"bearer"}

#####################################################################################
@app.get("/api/invoice/bankdetail/all", tags=['Bank Detail'])
def get_all_bank_details(db: Session = Depends(get_db), user_info: dict = Depends(get_current_user_info)):
    return db.query(models.BankDetail).all()

@app.put("/api/invoice/bankdetail/{guid}/update", response_model=schemas.BankDetailUpdate, status_code=status.HTTP_202_ACCEPTED, tags=['Bank Detail'])
def update_bank_detail(guid: str, request: schemas.BankDetailUpdate, db: Session = Depends(get_db)):
    invoice = db.query(models.BankDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.account_fname:
        invoice.account_fname = request.account_fname
    if request.account_lname:
        invoice.account_lname = request.account_lname
    if request.bank_address:
        invoice.bank_address = request.bank_address
    if request.bank_country:
        invoice.bank_country = request.bank_country
    if request.bank_email:
        invoice.bank_email = request.bank_email
    if request.bank_ifsc_code:
        invoice.bank_ifsc_code = request.bank_ifsc_code
    if request.bank_phone_number:
        invoice.bank_phone_number = request.bank_phone_number
    db.commit()
    return invoice

@app.post("/api/invoice/bankdetail/create", response_model=schemas.BankDetailCreateView, status_code=status.HTTP_201_CREATED, tags=['Bank Detail'])
def create_bank_detail(request: schemas.BankDetailCreate, db: Session = Depends(get_db)):
    invoice = models.BankDetail(guid=guid_gen(), account_company_name=request.account_company_name, account_fname=request.account_fname, account_lname=request.account_lname, bank_ifsc_code=request.bank_ifsc_code,
                                bank_address=request.bank_address, bank_country=request.bank_country, bank_phone_number=request.bank_phone_number, bank_email=request.bank_email)
    if not db.query(models.BankDetail).filter(BankDetail.account_company_name == request.account_company_name).first():
        try:
            # invoice = models.BankDetail(account_company_name=request.account_company_name,account_fname=request.account_fname, account_lname=request.account_lname, bank_ifsc_code=request.bank_ifsc_code, bank_address=request.bank_address, bank_country=request.bank_country, bank_phone_number=request.bank_phone_number, bank_email=request.bank_email )
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            # db.rollback(invoice.account_company_name)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists! from else ')

@app.delete("/api/invoice/bankkdetail/{guid}/delete", tags=['Bank Detail'])
def delete_bank_detail(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.BankDetail).filter(models.BankDetail.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.BankDetail).filter(models.BankDetail.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Bank Information Deleted Successfully!'}

@app.get("/api/invoice/bankdetail/{guid}", response_model=schemas.BankDetailCreate, tags=['Bank Detail'])
def get_bank_detail_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.BankDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
##########################################################################
@app.get("/api/invoice/client/all", tags=['Clients'])
def get_all_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.put("/api/invoice/client/{guid}/update", response_model=schemas.ClientCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Clients'])
def update_client(guid: str, request: schemas.ClientCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.Client).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.client_company_name:
        invoice.client_company_name = request.client_company_name
    if request.client_contact_name:
        invoice.client_contact_name = request.client_contact_name
    if request.client_contact_designation:
        invoice.client_contact_designation = request.client_contact_designation
    if request.client_city:
        invoice.client_city = request.client_city
    if request.client_state:
        invoice.client_state = request.client_state
    if request.client_pincode:
        invoice.client_pincode = request.client_pincode
    if request.client_country:
        invoice.client_country = request.client_country
    if request.client_phone_no:
        invoice.client_phone_no = request.client_phone_no
    if request.client_email:
        invoice.client_email = request.client_email
    if request.client_state_code:
        invoice.client_state_code = request.client_state_code
    if request.client_gstin:
        invoice.client_gstin = request.client_gstin

    db.commit()
    return invoice

@app.post("/api/invoice/client/create", status_code=status.HTTP_201_CREATED, tags=['Clients'])
def create_client(request: schemas.ClientCreate, db: Session = Depends(get_db)):
    invoice = models.Client(guid=guid_gen(), client_company_name=request.client_company_name, client_contact_name=request.client_contact_name, client_contact_designation=request.client_contact_designation, client_city=request.client_city, client_state=request.client_state, client_pincode=request.client_pincode, 
                            client_country=request.client_country, client_phone_no=request.client_phone_no, client_email=request.client_email, client_state_code=request.client_state_code, client_gstin=request.client_gstin)
    if not db.query(models.Client).filter(Client.client_company_name == request.client_company_name).first():
        try:
            # invoice = models.BankDetail(account_company_name=request.account_company_name,account_fname=request.account_fname, account_lname=request.account_lname, bank_ifsc_code=request.bank_ifsc_code, bank_address=request.bank_address, bank_country=request.bank_country, bank_phone_number=request.bank_phone_number, bank_email=request.bank_email )
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            # db.rollback(invoice.account_company_name)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/client/{guid}/delete", tags=['Clients'])
def delete_client(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Client).filter(models.Client.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.Client).filter(models.Client.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/client/{guid}",  tags=['Clients'])
def get_bank_detail_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Client).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
##############################################################################

@app.get("/api/invoice/stockdetail/all", tags=['Stock Detail'])
def get_all_stock_detail(db: Session = Depends(get_db)):
    return db.query(models.StockDetail).all()

@app.put("/api/invoice/stockdetail/{guid}/update", response_model=schemas.StockDetailCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Stock Detail'])
def update_stock_detail(guid: str, request: schemas.StockDetailCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.StockDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.stock_name:
        invoice.stock_name = request.stock_name
    db.commit()
    return invoice

@app.post("/api/invoice/stockdetail/create", status_code=status.HTTP_201_CREATED, tags=['Stock Detail'])
def create_stock_detail(request: schemas.StockDetailCreate, db: Session = Depends(get_db)):
    invoice = models.StockDetail(guid=guid_gen(), stock_name=request.stock_name)
    if not db.query(models.StockDetail).filter(StockDetail.stock_name == request.stock_name).first():
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/stockdetail/{guid}/delete", tags=['Stock Detail'])
def delete_stock_detail(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.StockDetail).filter(models.StockDetail.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.StockDetail).filter(models.StockDetail.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/stockdetail/{guid}",  tags=['Stock Detail'])
def get_stock_detail_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.StockDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
###################################################################

@app.get("/api/invoice/stockbatchinfo/all", tags=['Stock Batch Info'])
def get_all_stock_batch_info(db: Session = Depends(get_db)):
    return db.query(models.StockBatchInfo).all()

@app.put("/api/invoice/stockbatchinfo/{guid}/update", response_model=schemas.StockBatchInfoCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Stock Batch Info'])
def update_stock_batch_info(guid: str, request: schemas.StockBatchInfoCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.StockBatchInfo).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.stock_name:
        invoice.stock_name = request.stock_name
    db.commit()
    return invoice

@app.post("/api/invoice/stockbatchinfo/create", status_code=status.HTTP_201_CREATED, tags=['Stock Batch Info'])
def create_stock_batch_info(request: schemas.StockBatchInfoCreate, db: Session = Depends(get_db)):
    invoice = models.StockBatchInfo(guid=guid_gen(), stock_name=request.stock_name)
    if not db.query(models.StockBatchInfo).filter(StockBatchInfo.stock_name == request.stock_name).first():
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/stockbatchinfo/{guid}/delete", tags=['Stock Batch Info'])
def delete_stock_batch_info(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.StockBatchInfo).filter(models.StockBatchInfo.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.StockBatchInfo).filter(models.StockBatchInfo.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/stockbatchinfo/{guid}",  tags=['Stock Batch Info'])
def get_stock_batch_info_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.StockBatchInfo).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
############################################################################
@app.get("/api/invoice/itemdetail/all", tags=['Item Detail'])
def get_all_item_detail(db: Session = Depends(get_db)):
    return db.query(models.ItemDetail).all()

@app.put("/api/invoice/itemdetail/{guid}/update", response_model=schemas.ItemDetailCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Item Detail'])
def update_stock_batch_info(guid: str, request: schemas.ItemDetailCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.ItemDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.invoice_item_qty:
        invoice.invoice_item_qty = request.invoice_item_qty
    if request.invoice_item_taxable_value:
        invoice.invoice_item_taxable_value = request.invoice_item_taxable_value
    if request.invoice_item_tag_no:
        invoice.invoice_item_tag_no = request.invoice_item_tag_no
    if request.invoice_item_currency:
        invoice.invoice_item_currency = request.invoice_item_currency
    db.commit()
    return invoice

@app.post("/api/invoice/itemdetail/create", status_code=status.HTTP_201_CREATED, tags=['Item Detail'])
def create_item_detail(request: schemas.ItemDetailCreate, db: Session = Depends(get_db)):
    invoice = models.ItemDetail(guid=guid_gen(), invoice_item_qty=request.invoice_item_qty, invoice_item_taxable_value=request.invoice_item_taxable_value, invoice_item_tag_no=request.invoice_item_tag_no, invoice_item_currency=request.invoice_item_currency)
    if not False:
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/itemdetail/{guid}/delete", tags=['Item Detail'])
def delete_item_detail(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.ItemDetail).filter(models.ItemDetail.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.ItemDetail).filter(models.ItemDetail.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/itemdetail/{guid}",  tags=['Item Detail'])
def get_item_detail_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.ItemDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
###########################################################

@app.get("/api/invoice/terms/all", tags=['Terms And Conditions'])
def get_all_TNC(db: Session = Depends(get_db)):
    return db.query(models.TermsAndConditions).all()

@app.put("/api/invoice/terms/{guid}/update", response_model=schemas.TermsAndConditionsCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Terms And Conditions'])
def update_TNC(guid: str, request: schemas.TermsAndConditionsCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.TermsAndConditions).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.tac_description:
        invoice.tac_description = request.tac_description
    db.commit()
    return invoice

@app.post("/api/invoice/terms/create", status_code=status.HTTP_201_CREATED, tags=['Terms And Conditions'])
def create_TNC(request: schemas.TermsAndConditionsCreate, db: Session = Depends(get_db)):
    invoice = models.TermsAndConditions(guid=guid_gen(), tac_description=request.tac_description)
    if not db.query(models.TermsAndConditions).filter(TermsAndConditions.tac_description == request.tac_description).first():
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/terms/{guid}/delete", tags=['Terms And Conditions'])
def delete_TNC(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.TermsAndConditions).filter(models.TermsAndConditions.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.TermsAndConditions).filter(models.TermsAndConditions.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/terms/{guid}",  tags=['Terms And Conditions'])
def get_TNC_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.TermsAndConditions).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
###########################################################
@app.get("/api/invoice/signatory/all", tags=['Signatory'])
def get_all_signatory(db: Session = Depends(get_db)):
    return db.query(models.Signatory).all()

@app.put("/api/invoice/signatory/{guid}/update", response_model=schemas.SignatoryCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Signatory'])
def update_signatory(guid: str, request: schemas.SignatoryCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.Signatory).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.signatory_name:
        invoice.signatory_name = request.signatory_name
    if request.signatory_img_b64:
        invoice.signatory_img_b64 = request.signatory_img_b64
    db.commit()
    return invoice

@app.post("/api/invoice/signatory/create", status_code=status.HTTP_201_CREATED, tags=['Signatory'])
def create_signatory(request: schemas.SignatoryCreate, db: Session = Depends(get_db)):
    invoice = models.Signatory(guid=guid_gen(), signatory_name=request.signatory_name, signatory_img_b64=request.signatory_img_b64)
    if not db.query(models.Signatory).filter(Signatory.signatory_name == request.signatory_name).first():
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/signatory/{guid}/delete", tags=['Signatory'])
def delete_signatory(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Signatory).filter(models.Signatory.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.Signatory).filter(models.Signatory.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/signatory/{guid}",  tags=['Signatory'])
def get_Signatory_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Signatory).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
##################################################################################

@app.get("/api/invoice/taxation/all", tags=['Taxation'])
def get_all_taxation(db: Session = Depends(get_db)):
    return db.query(models.Taxation).all()

@app.put("/api/invoice/taxation/{guid}/update", response_model=schemas.TaxationCreate, status_code=status.HTTP_202_ACCEPTED, tags=['Taxation'])
def update_taxation(guid: str, request: schemas.TaxationCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.Taxation).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.policy_no:
        invoice.policy_no = request.policy_no
    if request.freight_terms:
        invoice.freight_terms = request.freight_terms
    if request.tax_component_1:
        invoice.tax_component_1 = request.tax_component_1
    if request.tax_component_2:
        invoice.tax_component_2 = request.tax_component_2
    if request.tax_component_3:
        invoice.tax_component_3 = request.tax_component_3
    db.commit()
    return invoice

@app.post("/api/invoice/taxation/create", status_code=status.HTTP_201_CREATED, tags=['Taxation'])
def create_taxation(request: schemas.TaxationCreate, db: Session = Depends(get_db)):
    invoice = models.Taxation(guid=guid_gen(), policy_no=request.policy_no, freight_terms=request.freight_terms, tax_component_1=request.tax_component_1, tax_component_2=request.tax_component_2, tax_component_3=request.tax_component_3)
    if not db.query(models.Taxation).filter(Taxation.policy_no == request.policy_no).first():
        try:
            print(request)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice

        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This record already exists!')

@app.delete("/api/invoice/taxation/{guid}/delete", tags=['Taxation'])
def delete_taxation(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Taxation).filter(models.Taxation.guid==guid).first()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(models.Taxation).filter(models.Taxation.guid == guid).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Deleted Successfully!'}

@app.get("/api/invoice/taxation/{guid}",  tags=['Taxation'])
def get_taxation_by_id(guid: str, db: Session = Depends(get_db)):
    invoice = db.query(models.Taxation).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice
##################################################################################


