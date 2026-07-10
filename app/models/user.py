from datetime import datetime

from sqlalchemy import String,DateTime,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

is_active: Mapped[bool] = mapped_column(
  Boolean,
  default=True,
)

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)

  username: Mapped[str] = mapped_column(
    String(100),
    unique=True,
    nullable=False
  )

  email: Mapped[str] = mapped_column(
    String(255),
    unique=True,
    nullable=False
  )

  hashed_password: Mapped[str] = mapped_column(
    String(255),
    nullable=False
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow,
  )

  jobs = relationship(
    "Job",
    back_populates="user",
    cascade="all, delete-orphan",
  )
  
