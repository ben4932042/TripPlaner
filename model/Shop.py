from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import Column, VARCHAR, UniqueConstraint, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shop(Base):
    """ shop name table detail"""
    __tablename__ = 'shop'
    id = Column(BIGINT(20), primary_key=True, autoincrement=True)
    uuid = Column(VARCHAR(60), primary_key=True)
    shop_name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
