import datetime

from sqlalchemy import select, and_, Date, cast, between, delete
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import days_off, registers_date, registers


async def add_day_off(master_id: int, start_date: datetime.date, stop_date: datetime.date):
    with engine.connect() as db:
        db.execute(
            insert(days_off).
            values(masters_id_pk=master_id, start_date=start_date, stop_date=stop_date)
        )
        db.commit()


async def get_days_off(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                days_off.c.start_date,
                days_off.c.stop_date
            ).
            where(days_off.c.masters_id_pk == master_id)
        )
        query = db.execute(query).fetchall()
        return query


async def delete_days_off(master_id: int, start_date: datetime.date, stop_date: datetime.date):
    with engine.connect() as db:
        db.execute(
            delete(days_off).
            where(
                and_(
                    days_off.c.masters_id_pk == master_id,
                    days_off.c.start_date == start_date,
                    days_off.c.stop_date == stop_date
                )
            )
        )
        db.commit()


async def get_registers(master_id: int, start_date: datetime.date, stop_date: datetime.date) -> list:
    with engine.connect() as db:
        query = (
            select(registers_date.c.start_service).
            group_by(registers_date.c.start_service).
            join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk).
            where(
                and_(
                    registers.c.masters_id_pk == master_id,
                    between(registers_date.c.start_service.cast(Date), start_date, stop_date)
                )
            ).
            order_by(registers_date.c.start_service)
        )
        return db.execute(query).scalars().all()
