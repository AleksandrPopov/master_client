from datetime import datetime

from sqlalchemy import select, exists, func, update, delete
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import masters, messages, schedules


async def get_master(master_id: int) -> tuple:
    with engine.connect() as db:
        query = select(
            masters.c.name,
            masters.c.contact
        ).where(masters.c.id == master_id)
        return db.execute(query).fetchone()


async def is_master_exists(master_id: int) -> tuple:
    with engine.connect() as db:
        query = (select(exists(masters).where(masters.c.id == master_id)))
        return db.execute(query).scalar()


async def get_counts_masters():
    with engine.connect() as db:
        query = select(func.count()).select_from(masters)
        return db.execute(query).scalar()


async def add_master(master_id: int, master_name: str, master_contact: str):
    # TODO: Delete on_conflict_do_nothing().
    with engine.connect() as db:
        db.execute(
            insert(masters).
            values(id=master_id, name=master_name, contact=master_contact).
            on_conflict_do_nothing()
        )
        for i in range(7):
            db.execute(
                insert(schedules).
                values(
                    masters_id_pk=master_id,
                    day=i,
                    start_time=datetime.now().time().min,
                    stop_time=datetime.now().time().min
                )
            )
        db.commit()


async def change_master_name(master_id: int, name: str) -> tuple:
    with engine.connect() as db:
        query = db.execute(
            update(masters).
            where(masters.c.id == master_id).
            values(name=name).
            returning(masters.c.name, masters.c.contact)
        )
        db.commit()
        return query.fetchone()


async def change_master_contact(master_id: int, contact: str) -> tuple:
    with engine.connect() as db:
        query = db.execute(
            update(masters).
            where(masters.c.id == master_id).
            values(contact=contact).
            returning(masters.c.name, masters.c.contact)
        )
        db.commit()
        return query.fetchone()


async def delete_account(master_id: int):
    with engine.connect() as db:
        db.execute(
            delete(masters).
            where(
                masters.c.id == master_id
            )
        )
        db.commit()
