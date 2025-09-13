from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Registro(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'api'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)      # n sei se esse index pode cagar
    email = Column(String)
    password = Column(String)