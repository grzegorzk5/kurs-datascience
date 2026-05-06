from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import MovieBase
from .associations import movie_actor_association

class Actor(MovieBase):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    movies = relationship('Movie', secondary=movie_actor_association, back_populates='actors')

    def __repr__(self):
        return f"<Actor(name='{self.name}', movies={len(self.movies)})>"