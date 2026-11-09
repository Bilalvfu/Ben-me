from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    movies = relationship("Movie", back_populates="owner")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String)
    release_year = Column(Integer)
    genre = Column(String, index=True)
    watched = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="movies")
