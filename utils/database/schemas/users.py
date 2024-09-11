from utils.database.db import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(255), primary_key=True)


    query: sql.select


