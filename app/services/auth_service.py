from sqlalchemy.orm import Session

from app.models.user import  User
from app.schemas.user import UserRegister
from app.core.security import hash_password

class AuthService:
  @staticmethod
  def register(db: Session, user_data: UserRegister):
    existing_user = (
      db.query(User)
      .filter(User.email == user_data.email)
      .first()
    )

    if existing_user:
      raise ValueError("Email already registered.")
    
    user = User(
      username=user_data.username,
      email=user_data.email,
      hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user