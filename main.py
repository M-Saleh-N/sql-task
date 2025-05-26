from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select

# Define your PostgreSQL connection URL
# Replace `user`, `password`, `localhost`, and `dbname` with your actual values
DATABASE_URL = "postgresql+psycopg2://postgres:657844@localhost/myydbb"

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Define the User model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

# Create the database tables
def create_db():
    SQLModel.metadata.create_all(engine)

# Create a new user
def create_user(name: str, email: str):
    with Session(engine) as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Created: {user}")

# Read all users
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print("All users:")
        for user in users:
            print(user)

# Update a user by ID
def update_user(user_id: int, new_name: str):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            user.name = new_name
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"Updated: {user}")
        else:
            print("User not found")

# Delete a user by ID
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            print(f"Deleted user with ID: {user_id}")
        else:
            print("User not found")

# Example usage
if __name__ == "__main__":
    create_db()
    create_user("Alice", "alice@example.com")
    create_user("Bob", "bob@example.com")
    read_users()
    update_user(1, "Alicia")
    delete_user(2)
    read_users()
