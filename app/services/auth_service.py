from sqlalchemy.orm import Session

from app.models.user import  User
from app.schemas.user import UserRegister
from app.core.security import hash_password, verify_password

class AuthService:

  @staticmethod
  def register(db: Session, user_data: UserRegister):
  
      if db.query(User).filter(User.email == user_data.email).first():
         raise ValueError("Email already exists.")
    

    
      
      
      if db.query(User).filter(User.username == user_data.username).first():

        raise ValueError("Username already exists.")

      user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
      )

      db.add(user)
      db.commit()
      db.refresh(user)

      return user
  
  @staticmethod
  def authenticate(
      db: Session,
      email: str,
      password: str,
  ):
     
      user = db.query(User).filter(
          User.email == email
      ).first()

      if not user:
         return None
      
      if not verify_password(
         password,
         user.hashed_password
      ):
         return None
      
      return user
      