from sqlalchemy import Table, Column, Integer, Numeric, String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()


class Buy(Base):
    __tablename__ = 'buy'
    buy_id = Column(Integer(), primary_key=True)
    username = Column(String(15),ForeignKey('users.username'))
    phone = Column(String(20),ForeignKey('users.phone'))
    data_city = Column(String(20))
    data_time = Column(String(20))
    city = Column(String(125))
    menu = Column(String(25))
    price = Column(Integer())
    calendar= Column(String(10))
    created_on = Column(DateTime(), default=datetime.now)

def __ini__(self, buy_id,username,phone,data_city,data_time,menu,price,city,calendar,created_on):
        self.buy_id = buy_id
        self.username = username
        self.phone = phone
        self.data_city = data_city
        self.data_time = data_time
        self.menu = menu
        self.price = price
        self.city = city
        self.calendar = calendar
        self.created_on = created_on


def __repr__(self):
    return "Buy(username='{self.username}', " \
"phone='{self.phone}', " \
"city='{self.city}', " \
"data_city='{self.data_city}', " \
"data_time='{self.data_time}', " \
"calendar='{self.calendar}', " \
"price='{self.price}', " \
"menu='{self.menu}')".format(self=self)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15))
    email_address = Column(String(255))
    phone = Column(String(20))
    token = Column(String(25))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


def __ini__(self, user_id, username, email_address, phone, token, created_on, updated_on):
    self.user_id = user_id
    self.username = username
    self.email_address = email_address
    self.phone = phone
    self.token = token
    self.created_on = created_on
    self.updated_on = updated_on


def __repr__(self):
    return "User(username='{self.username}', " \
           "email_address='{self.email_address}', " \
           "phone='{self.phone}', " \
           "token='{self.token}')".format(self=self)