# from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    header = Column(String(20))
    description = Column(String(150))
    created_at = Column(DateTime, insert_default=func.now())

    columnes_count = 4