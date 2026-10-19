from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return 'rashad this is your beginning to fastapi'

products = [
    Product(id=1, name='phone', description='budget phone', price='99', quantity=10),
    Product(id=2, name='laptop', description='budget lap', price='19', quantity=120),
    Product(id=3, name='mobile', description='budget mobile', price='9', quantity=110),
    Product(id=4, name='pen', description='budget pen', price='3', quantity=105),
    Product(id=5, name='table', description='budget table', price='9', quantity=130),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    # for product in products:
    #     db.add(database_models.Product(**product.model_dump()))
    db.commit()

init_db()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    # db.query(Product.)
    return db_products


@app.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return 'product not found'


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db.commit()
        return 'product updated'
    return 'product not found'

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return 'product deleted'
    return 'product not found'
