from sqlalchemy import Boolean, Column, Integer, String, Date

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    text = Column(String, nullable=False)
    completion_date = Column(Date)
    is_completed = Column(Boolean, default=False)
