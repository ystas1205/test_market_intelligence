from sqlalchemy import Column, Integer, String, \
    MetaData, func, UUID, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(String, index=True, nullable=False)
    code_phrase = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    date_of_creation = Column(DateTime, default=func.current_timestamp())
    TTL = Column(Integer, nullable=False)
