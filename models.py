from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey,Boolean
from sqlalchemy.orm import declarative_base

db = create_engine('sqlite:///data.db')

base = declarative_base()

class User(base):
    __tablename__ = 'user'
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    name = Column("name",String)
    email = Column("email",String,unique=True)
    password = Column("password",String)
    created_at = Column("created_at",Date)
    status = Column("status",Boolean, default=True)
    admin = Column("admin",Boolean, default=False)

class form(base):
    __tablename__ = 'form'
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id",Integer, ForeignKey('user.id'))
    file = Column("file",String)






