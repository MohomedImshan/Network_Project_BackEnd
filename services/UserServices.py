from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.User import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_user(db: Session, firstName: str, lastName: str, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None, "Email already registered"

    # Truncate password to 72 chars
    hashed_password = pwd_context.hash(password)

    # Correct field names here
    new_user = User(
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user, None
