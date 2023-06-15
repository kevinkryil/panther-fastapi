from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panther")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/api/invoice/all", tags=['Invoice'])
def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()

@app.post("/api/invoice/create", response_model=schemas.Invoice, status_code=status.HTTP_201_CREATED, tags=['Invoice'])
def create_invoice(request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = models.Invoice(product=request.product)
    db.add(invoice)
    db.commit()
    db.refresh(invoice) 
    return invoice

@app.put("/api/invoice/{id}/update", response_model=schemas.Invoice, status_code=status.HTTP_202_ACCEPTED, tags=['Invoice'])
def update_invoice(id: int, request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.product:
        invoice.product = request.product
    db.commit()
    return invoice

@app.delete("/api/invoice/{id}/delete", tags=['Invoice'])
def delete_invoice(id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    db.query(models.Invoice).filter(models.Invoice.id==id).delete(synchronize_session=False)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.commit()
    return {'msg':'Invoice Deleted Successfully!'}
    
@app.get("/api/invoice/{id}", response_model=schemas.Invoice, tags=['Invoice'])
def get_invoice_by_id(id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice





