from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import MovieBase
from .associations import movie_actor_association

class Movie(MovieBase):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))

    actors = relationship('Actor', secondary=movie_actor_association, back_populates='movies')

    def __repr__(self):
        return f"<Movie(title='{self.title}', actors={len(self.actors)})>"
