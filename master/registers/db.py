from datetime import datetime

from sqlalchemy import select, Date, extract, distinct, and_, func, Time, delete

from database.connector import engine
from database.tables import registers_date, registers, schedules, masters, clients, services, categories


async def get_registers_date(master_id: int, month: int, year: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                registers_date.c.start_service.cast(Date)
            ).select_from(
                registers.
                join(registers_date, registers.c.registers_date_id_pk == registers_date.c.id)
            ).
            where(
                and_(
                    registers.c.masters_id_pk == master_id,
                    extract('month', registers_date.c.start_service) == month,
                    extract('year', registers_date.c.start_service) == year,
                )
            ).
            order_by(
                registers_date.c.start_service.cast(Date)
            )
        )
        return db.execute(query).scalars().all()


async def get_registers_months(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                distinct(func.date_trunc('month', registers_date.c.start_service).cast(Date))
            ).
            select_from(
                registers.
                join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk)
            ).
            where(registers.c.masters_id_pk == master_id)
        )
        return db.execute(query).scalars().all()


async def get_schedule(master_id: int, day: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                schedules.c.start_time,
                schedules.c.stop_time
            ).
            where(
                and_(
                    schedules.c.masters_id_pk == master_id,
                    schedules.c.day == day
                )
            )
        )
        return db.execute(query).fetchall()


async def get_registers_times(master_id: int, date: datetime.date) -> list:
    with engine.connect() as db:
        query = (
            select(
                registers.c.registers_date_id_pk,
                registers_date.c.start_service.cast(Time)
            ).
            select_from(
                registers.
                join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk)
            ).
            where(
                and_(
                    registers.c.masters_id_pk == master_id,
                    registers_date.c.start_service.cast(Date) == date
                )
            ).
            group_by(
                registers.c.registers_date_id_pk,
                registers_date.c.start_service.cast(Time)
            ).
            order_by(
                registers_date.c.start_service.cast(Time)
            )
        )
        return db.execute(query).fetchall()


async def get_register_by_id(register_id: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                registers.c.registers_date_id_pk,
                masters.c.id,
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
                registers.c.registers_date_id_pk == register_id
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
        return db.execute(query).fetchone()


async def get_register(register_id: int):
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
                registers.c.registers_date_id_pk == register_id
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
        return db.execute(query).fetchone()


async def delete_register(register_id: int):
    with engine.connect() as db:
        db.execute(
            delete(registers).
            where(registers.c.registers_date_id_pk == register_id)
        )
        db.execute(
            delete(registers_date).
            where(registers_date.c.id == register_id)
        )
        db.commit()
