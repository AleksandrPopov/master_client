from datetime import datetime, timedelta

from sqlalchemy import select, and_, func, delete, literal_column, distinct, Date, Time

from config import TZ
from database.connector import engine
from database.tables import masters, clients, categories, services, registers_date, registers


async def get_registers(client_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                registers.c.registers_date_id_pk,
                masters.c.id,
                masters.c.name,
                clients.c.name,
                clients.c.contact,
                func.string_agg(categories.c.name, ', '),
                func.string_agg(services.c.name, ', '),
                func.sum(services.c.cost),
                registers_date.c.start_service,
                registers_date.c.stop_service,
            ).
            select_from(
                registers.
                join(masters, masters.c.id == registers.c.masters_id_pk).
                join(clients, clients.c.id == registers.c.client_table_id_pk).
                join(services, services.c.id == registers.c.service_id_pk).
                join(categories, categories.c.id == services.c.categories_id_pk).
                join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk)
            ).
            where(
                registers.c.clients_id_pk == client_id
            ).
            group_by(
                registers.c.registers_date_id_pk,
                masters.c.id,
                masters.c.name,
                clients.c.name,
                clients.c.contact,
                registers_date.c.start_service,
                registers_date.c.stop_service,
            ).
            order_by(
                registers_date.c.start_service
            )
        )
        return db.execute(query).fetchall()


async def get_register_incoming():
    time = datetime.now(TZ).replace(second=0, microsecond=0, tzinfo=None) + timedelta(hours=1)
    with engine.connect() as db:
        query = (
            select(
                registers.c.registers_date_id_pk,
                clients.c.client_id,
                masters.c.name,
                clients.c.name,
                clients.c.contact,
                func.string_agg(categories.c.name, ', '),
                func.string_agg(services.c.name, ', '),
                func.sum(services.c.cost),
                registers_date.c.start_service,
                registers_date.c.stop_service,
            ).
            select_from(
                registers.
                join(masters, masters.c.id == registers.c.masters_id_pk).
                join(clients, clients.c.id == registers.c.client_table_id_pk).
                join(services, services.c.id == registers.c.service_id_pk).
                join(categories, categories.c.id == services.c.categories_id_pk).
                join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk)
            ).
            where(
                registers_date.c.start_service == time
            ).
            group_by(
                registers.c.registers_date_id_pk,
                clients.c.client_id,
                masters.c.id,
                masters.c.name,
                clients.c.name,
                clients.c.contact,
                registers_date.c.start_service,
                registers_date.c.stop_service,
            ).
            order_by(
                registers_date.c.start_service
            )
        )
        return db.execute(query).fetchall()


async def delete_register(register_id: int):
    with engine.connect() as db:
        db.execute(
            delete(registers_date).
            where(registers_date.c.id == register_id)
        )
        db.commit()


async def delete_register_after():
    time = datetime.now(TZ).replace(second=0, microsecond=0, tzinfo=None)
    with engine.connect() as db:
        db.execute(
            delete(registers_date).
            where(registers_date.c.stop_service <= time)
        )
        db.commit()
