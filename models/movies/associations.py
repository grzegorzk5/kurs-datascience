from sqlalchemy import Column, Integer, Table, ForeignKey
from .base import MovieBase

movie_actor_association = Table(
    'movie_actor',
    MovieBase.metadata,    
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)