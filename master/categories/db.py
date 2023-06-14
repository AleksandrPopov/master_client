from sqlalchemy import select, update, exists, and_, delete
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import categories


async def get_categories(master_id: int) -> tuple:
    with engine.connect() as db:
        query = (
            select(categories.c.id, categories.c.name).
            where(categories.c.masters_id_pk == master_id)
        )
        query = db.execute(query).fetchall()
        return query if query is not None else ()


async def get_category(category_id: int) -> str:
    with engine.connect() as db:
        query = (
            select(categories.c.name).
            where(categories.c.id == category_id)
        )
        return db.execute(query).scalar()


async def add_category(master_id: int, category_mame: str) -> bool:
    with engine.connect() as db:
        query = db.execute(
            insert(categories).
            values(masters_id_pk=master_id, name=category_mame).
            returning(categories.c.id, categories.c.name)
        )
        db.commit()
        return query.fetchone()


async def change_category_name(category_id: int, category_name: str):
    with engine.connect() as db:
        db.execute(
            update(categories).
            where(categories.c.id == category_id).
            values(name=category_name).
            returning(categories.c.name)
        )
        db.commit()


async def delete_category(category_id: int):
    with engine.connect() as db:
        db.execute(
            delete(categories).
            where(categories.c.id == category_id)
        )
        db.commit()
