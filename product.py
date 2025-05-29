from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select

# Define your PostgreSQL connection URL
# Replace `user`, `password`, `localhost`, and `dbname` with your actual values
DATABASE_URL = "postgresql+psycopg2://postgres:657844@localhost/myydbb"

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Define the Product model
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    img_url: str

# Create the database tables
def create_db():
    SQLModel.metadata.create_all(engine)

#CREATE A FUNCTION create_product THAT INSERTS DATA IN THE PRODUCT MODEL
def create_product(name: str, price: float, img_url: str):
    with Session(engine) as session:
        product = Product(name=name, price=price, img_url=img_url)
        session.add(product)
        session.commit()
        session.refresh(product)
        print(f"Created product: {product}")

#CREATE A FUNCTION read_product THAT FETCHES ALL THE DATA IN THE PRODUCT MODEL
def read_product():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products
    
# CREATE A FUNCTION update_product THAT UPDATES THE PRODUCT PRICE, NAME OR product_img_url
def update_product(id: int, name: Optional[str] = None, price : Optional[float] = None, img_url: Optional[str] = None):
    with Session(engine) as session:
        product = session.get(Product, id)
        if name:
            product.name = name
            if price:
                product.price = price
                if img_url:
                    product.img_url = img_url
                    session.commit()
                    print(f"Updated product: {product}")

# CREATE A FUNCTION delete_product THAT DELETES A PRODUCT BY ITS ID
def delete_product(id: int):
    with Session(engine) as session:
        product = session.get(Product, id)
        session.delete(product)
        session.commit()
        print(f"Deleted product: {id}")

# 






if __name__ == "__main__":
    create_db()
    create_product("Black Rose", 200, 'https://imgs.search.brave.com/I0-J_EDp7CLMe7mJSr2-CsxIQPV41N-Amh74zj-or80/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9yb3Nh/aG9saWNzLmNvbS9j/ZG4vc2hvcC9wcm9k/dWN0cy9CbGFja21h/bWJhMjAyMV81NGFi/MDBlYy0yZDJhLTRh/NjItOGRjNS0xYjMw/OGI3NGE0OTRfMTAy/NHgxMDI0LmpwZz92/PTE3MzkyMDc5MTM')
    read_product()
    update_product(1, name="Red Rose", price=300, img_url='https://www.canva.com/photos/s/rose/')
    delete_product(1)
    read_product()



