from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class wordcloud(Base):
    __tablename__ = "wordcloud"
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(5000), nullable=False)


class photo(Base):
    __tablename__ = "photo"
    photo_id = Column(Integer, primary_key=True, autoincrement=True)
    photo_url = Column(String(255))
