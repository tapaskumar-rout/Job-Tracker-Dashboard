from datetime import datetime,date

from sqlalchemy import String ,ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database.database import Base

class Job(Base):
  __tablename__ = "jobs"
  
  id: Mapped[int] = mapped_column(primary_key=True, index=True)

  company: Mapped[str] = mapped_column(String(100), nullable=False)

  job_title: Mapped[str] = mapped_column(String(100),nullable=False)

  location: Mapped[str] = mapped_column(String(100), nullable=True)

  status: Mapped[str] = mapped_column(
    String(30),
    default="Applied"
  )

  application_date: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow
  )

  notes: Mapped[str] = mapped_column(
    String(500),
    nullable=True
  )

  resume : Mapped[str] = mapped_column(
    String,
    nullable=True)

  user_id:Mapped[str] = mapped_column(
    ForeignKey("users.id")
  )

  user = relationship(
    "User",
    back_populates="jobs",
  )

  logo: Mapped[str | None] = mapped_column(
    String,
    nullable=True
  )              

  application_date: Mapped[date] = mapped_column(
    Date,
    default=date.today,
  )   

  priority: Mapped[str] = mapped_column(
    String(20),
    default="Medium",
  )

  follow_up_date: Mapped[date] = mapped_column(
    Date,
    nullable=True
  )