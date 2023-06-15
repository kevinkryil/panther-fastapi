from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Panther"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

#########################################################################################################################
@app.get("/api/invoice/all")
def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()

@app.post("/api/invoice/create", response_model=schemas.Invoice, status_code=status.HTTP_201_CREATED)
def create_invoice(request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = models.Invoice(product=request.product)
    db.add(invoice)
    db.commit()
    db.refresh(invoice) 
    return invoice

@app.put("/api/invoice/{id}/update", response_model=schemas.Invoice)
def update_invoice(id: int, request: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if request.product:
        invoice.product = request.product
    db.commit()
    return invoice

@app.delete("/api/invoice/{id}/delete")
def delete_invoice(id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    db.query(models.Invoice).filter(models.Invoice.id==id).delete(synchronize_session=False)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # db.delete(invoice)
    db.commit()
    return {'msg':'Invoice Deleted Successfully!'}
    
@app.get("/api/invoice/{id}", response_model=schemas.Invoice)
def get_invoice_by_id(id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoice





