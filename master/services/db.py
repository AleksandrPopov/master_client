from sqlalchemy import select, exists, and_, update, delete
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import categories, services


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


async def get_services(category_id: int) -> tuple:
    with engine.connect() as db:
        query = (
            select(services.c.id, services.c.name).
            where(services.c.categories_id_pk == category_id)
        )
        query = db.execute(query).fetchall()
        return query if query is not None else ()


async def get_service(service_id: int) -> tuple:
    with engine.connect() as db:
        query = (
            select(
                services.c.name,
                services.c.time,
                services.c.cost
            ).
            where(services.c.id == service_id)
        )
        return db.execute(query).fetchone()


async def exists_service_name(master_id: int, category_id: int, service_name: int) -> bool:
    with engine.connect() as db:
        query = (
            exists(services.c.name).
            where(
                and_(
                    services.c.masters_id_pk == master_id,
                    services.c.categories_id_pk == category_id,
                    services.c.name == service_name
                )
            ).select()
        )
        return db.execute(query).scalar()


async def add_service(master_id: int, category_id: str, service_name: str, service_time: str, service_cost: str) -> int:
    with engine.connect() as db:
        query = db.execute(
            insert(services).
            values(
                masters_id_pk=master_id,
                categories_id_pk=category_id,
                name=service_name,
                time=service_time,
                cost=service_cost
            ).
            returning(services.c.id)
        )
        db.commit()
        return query.scalar()


async def change_name_service(service_id: int, service_name: str):
    with engine.connect() as db:
        db.execute(
            update(services).
            where(services.c.id == service_id).
            values(name=service_name)
        )
        db.commit()


async def change_time_service(service_id: int, time: str):
    with engine.connect() as db:
        db.execute(
            update(services).
            where(services.c.id == service_id).
            values(time=time)
        )
        db.commit()


async def change_cost_service(service_id: int, cost: int):
    with engine.connect() as db:
        db.execute(
            update(services).
            where(services.c.id == service_id).
            values(cost=cost)
        )
        db.commit()


async def delete_service(service_id: int):
    with engine.connect() as db:
        db.execute(
            delete(services).
            where(services.c.id == service_id)
        )
        db.commit()
