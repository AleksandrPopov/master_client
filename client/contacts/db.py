from sqlalchemy import select, update, delete, exists

from database.connector import engine
from database.tables import clients, registers


async def get_contacts(client_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                clients.c.id,
                clients.c.name,
            ).
            where(clients.c.client_id == client_id)
        )
        return db.execute(query).fetchall()


async def get_contact(client_id: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                clients.c.id,
                clients.c.name,
                clients.c.contact
            ).
            where(clients.c.id == client_id)
        )
        return db.execute(query).fetchone()


async def delete_contact(client_id: int):
    with engine.connect() as db:
        db.execute(
            delete(clients).
            where(clients.c.id == client_id)
        )
        db.commit()


async def get_client_registers(client_id: int) -> bool:
    with engine.connect() as db:
        query = (
            exists(registers).
            where(registers.c.client_table_id_pk == client_id)
        ).select()
        return db.execute(query).scalar()


async def change_name(client_id: int, name: str):
    with engine.connect() as db:
        db.execute(
            update(clients).
            values(name=name).
            where(clients.c.id == client_id)
        )
        db.commit()


async def change_contact(client_id: int, contact: str):
    with engine.connect() as db:
        db.execute(
            update(clients).
            values(contact=contact).
            where(clients.c.id == client_id)
        )
        db.commit()
