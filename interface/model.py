from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class wordcloud(Base):
    __tablename__ = "wordcloud"
    content_id = Column(Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    content = Column(String(255), nullable=False)
