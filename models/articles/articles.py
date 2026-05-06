from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime


class ArticleBase(DeclarativeBase):
    pass

class Article(ArticleBase):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    published_date = Column(DateTime, nullable=True)
