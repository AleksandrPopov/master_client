from sqlalchemy import ForeignKey, MetaData, Table, Column, Sequence, text
from sqlalchemy import String, BigInteger, Time, Numeric, SmallInteger, Date, DateTime, JSON, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

meta = MetaData()

masters = Table('masters', meta,
                Column('id', BigInteger, primary_key=True),
                Column('name', String(64)),
                Column('contact', String(13))
                )

categories = Table('categories', meta,
                   Column('id', Integer, Sequence("categories_id_seq"), unique=True),
                   Column('masters_id_pk', BigInteger, ForeignKey('masters.id', ondelete='CASCADE'), primary_key=True),
                   Column('name', String(64), primary_key=True)
                   )

services = Table('services', meta,
                 Column('id', Integer,Sequence("services_id_seq"), unique=True),
                 Column('masters_id_pk', BigInteger, ForeignKey('masters.id', ondelete='CASCADE'), primary_key=True),
                 Column('categories_id_pk', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
                 Column('name', String(64), primary_key=True),
                 Column('time', Time),
                 Column('cost', Numeric(5, 2))
                 )

schedules = Table('schedules', meta,
                  Column('masters_id_pk', BigInteger, ForeignKey('masters.id', ondelete='CASCADE'), primary_key=True),
                  Column('day', SmallInteger, primary_key=True),
                  Column('start_time', Time),
                  Column('stop_time', Time)
                  )

days_off = Table('days_off', meta,
                 Column('masters_id_pk', BigInteger, ForeignKey('masters.id', ondelete='CASCADE'),primary_key=True),
                 Column('start_date', Date, primary_key=True),
                 Column('stop_date', Date, primary_key=True)
                 )

clients = Table('clients', meta,
                Column('id', Integer, Sequence("client_id_seq"), unique=True),
                Column('client_id', BigInteger, primary_key=True),
                Column('name', String(64), primary_key=True),
                Column('contact', String(13), primary_key=True)
                )

registers_date = Table('registers_date', meta,
                       Column('id', Integer, primary_key=True),
                       Column('start_service', DateTime),
                       Column('stop_service', DateTime)
                       )

registers = Table('registers', meta,
                  Column('id', BigInteger, primary_key=True),
                  Column('registers_date_id_pk', Integer,
                         ForeignKey("registers_date.id", ondelete='CASCADE', deferrable=True)),
                  Column('masters_id_pk', BigInteger, ForeignKey('masters.id', ondelete='CASCADE')),
                  Column('clients_id_pk', BigInteger),
                  Column('client_table_id_pk', Integer, ForeignKey('clients.id', ondelete='CASCADE')),
                  Column('service_id_pk', Integer, ForeignKey('services.id', ondelete='CASCADE'))
                  )

messages = Table('messages', meta,
                 Column('id', BigInteger, primary_key=True),
                 Column('role', String(6), primary_key=True),
                 Column('message_id', BigInteger, primary_key=True)
                 )

states = Table('states', meta,
               Column('user', BigInteger, primary_key=True),
               Column('chat', BigInteger),
               Column('role', String(6), primary_key=True),
               Column('state', String),
               Column('data', postgresql.JSONB)
               )

def create(engine: create_engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    meta.create_all(engine)
