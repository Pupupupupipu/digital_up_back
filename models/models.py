from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
import enum

Base = declarative_base()

class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)


class KindEnum(enum.Enum):
    film = "film"
    cartoon = "cartoon"
    serial = "serial"

class Film(Base):
    __tablename__ = "film"
    id = Column(Integer,Identity(start=1), primary_key=True)
    id_genre = Column(Integer, ForeignKey(Genre.id))
    kind = Column(ENUM(KindEnum, name="kind", create_type=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    trailer = Column(String, nullable=False)

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, login, hash_password):
        self.login = login
        self.hash_password = hash_password
        self.name = login


