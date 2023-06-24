from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from models import *

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

# @app.get("/api/invoice/all", tags=['Test'])
# def get_all_invoices(db: Session = Depends(get_db)):
#     return db.query(models.Invoice).all()


# @app.post("/api/invoice/create", response_model=schemas.Invoice, status_code=status.HTTP_201_CREATED, tags=['Test'])
# def create_invoice(request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
#     invoice = models.Invoice(product=request.product)
#     db.add(invoice)
#     db.commit()
#     db.refresh(invoice)
#     return invoice


# @app.put("/api/invoice/{id}/update", response_model=schemas.Invoice, status_code=status.HTTP_202_ACCEPTED, tags=['Test'])
# def update_invoice(id: int, request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
#     invoice = db.query(models.Invoice).get(id)
#     if not invoice:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     if request.product:
#         invoice.product = request.product
#     db.commit()
#     return invoice


# @app.delete("/api/invoice/{id}/delete", tags=['Test'])
# def delete_invoice(id: int, db: Session = Depends(get_db)):
#     invoice = db.query(models.Invoice).get(id)
#     db.query(models.Invoice).filter(models.Invoice.id ==
#                                     id).delete(synchronize_session=False)
#     if not invoice:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     db.commit()
#     return {'msg': 'Invoice Deleted Successfully!'}


# @app.get("/api/invoice/{id}", response_model=schemas.Invoice, tags=['Test'])
# def get_invoice_by_id(id: int, db: Session = Depends(get_db)):
#     invoice = db.query(models.Invoice).get(id)
#     if not invoice:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return invoice


#######################################################################################



@app.get("/api/invoice/bankdetail/all", tags=['Bank Detail'])
def get_all_bank_details(db: Session = Depends(get_db)):
    return db.query(models.BankDetail).all()


@app.put("/api/invoice/bankdetail/{guid}/update", response_model=schemas.BankDetailUpdate, status_code=status.HTTP_202_ACCEPTED, tags=['Bank Detail'])
def update_invoice(guid: str, request: schemas.BankDetailUpdate, db: Session = Depends(get_db)):
    invoice = db.query(models.BankDetail).get(guid)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # if request.account_company_name:
    #     invoice.account_company_name = request.account_company_name
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


@app.delete("/api/invoice/{guid}/delete", tags=['Bank Detail'])
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
