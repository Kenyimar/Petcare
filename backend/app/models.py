from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False)
    content_type = Column(String(20), nullable=False)
    summary = Column(String(300), nullable=False)
    body = Column(Text, nullable=False)