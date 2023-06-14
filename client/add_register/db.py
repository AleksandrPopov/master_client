from datetime import datetime

from sqlalchemy import select, exists, func, and_, extract, Date
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import masters, clients, services, categories, days_off, schedules, registers_date, registers


async def get_masters() -> list:
    with engine.connect() as db:
        query = (
            select(
                masters.c.id,
                masters.c.name,
                masters.c.contact
            ).
            group_by(masters.c.id).
            join(services).
            where(services.c.masters_id_pk == masters.c.id)
        )
        return db.execute(query).fetchall()


async def get_master(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                masters.c.id,
                masters.c.name,
                masters.c.contact
            ).
            where(masters.c.id == master_id)
        )
        return db.execute(query).fetchone()


async def add_client(client_id: int, client_name: str, client_contact: str):
    with engine.connect() as db:
        db.execute(
            insert(clients).
            values(client_id=client_id, name=client_name, contact=client_contact)
        )
        db.commit()


async def get_client_exists(client_id: int) -> bool:
    with engine.connect() as db:
        query = (
            select(
                exists(clients).
                where(clients.c.client_id == client_id)
            )
        )
        return db.execute(query).scalar()


async def get_clients(client_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                clients.c.id,
                clients.c.name,
                clients.c.contact
            ).
            where(clients.c.client_id == client_id)
        )
        return db.execute(query).fetchall()


async def get_client(client_id: int) -> dict:
    with engine.connect() as db:
        query = (
            select(clients).
            where(clients.c.id == client_id)
        )
        return db.execute(query).fetchone()


async def get_categories(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                categories.c.id,
                categories.c.name,
            ).
            where(categories.c.masters_id_pk == master_id)
        )
        return db.execute(query).fetchall()


async def get_category(category_id: int) -> tuple:
    with engine.connect() as db:
        query = (
            select(
                categories.c.id,
                categories.c.name,
            ).
            where(categories.c.id == category_id)
        )
        return db.execute(query).fetchone()


async def get_services(category_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                services.c.id,
                services.c.name,
            ).
            where(services.c.categories_id_pk == category_id)
        )
        return db.execute(query).fetchall()


async def services_sum_time(services_ids: list):
    with engine.connect() as db:
        query = (
            select(
                func.sum(services.c.time)
            ).
            where(services.c.id.in_(services_ids))
        )
        return db.execute(query).scalar()


async def get_schedules(master_id: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                schedules.c.day,
                schedules.c.start_time,
                schedules.c.stop_time
            ).
            where(schedules.c.masters_id_pk == master_id).
            order_by(schedules.c.day)
        )
        return db.execute(query).fetchall()


async def get_schedule(master_id: int, day: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                schedules.c.day,
                schedules.c.start_time,
                schedules.c.stop_time
            ).
            where(
                and_(
                    schedules.c.masters_id_pk == master_id,
                    schedules.c.day == day)
                )
        )
        return db.execute(query).fetchone()


async def get_days_off(master_id: int, year: int, month: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                days_off.c.start_date,
                days_off.c.stop_date,
            ).
            where(
                and_(
                    days_off.c.masters_id_pk == master_id,
                    extract('year', days_off.c.start_date) == year,
                    extract('month', days_off.c.start_date) == month
                )
            )
        )
        return db.execute(query).fetchall()


async def get_registers(master_id: int, date: datetime.date) -> list:
    with engine.connect() as db:
        query = (
            select(
                registers_date.c.start_service,
                registers_date.c.stop_service
            ).
            group_by(
                registers_date.c.start_service,
                registers_date.c.stop_service
            ).
            join(
                registers_date, registers_date.c.id == registers.c.registers_date_id_pk
            ).
            where(
                and_(
                    registers.c.masters_id_pk == master_id,
                    registers_date.c.start_service.cast(Date) == date
                )
            )
        )
        return db.execute(query).fetchall()


async def get_registers_date(master_id: int, month: int, year: int) -> list:
    with engine.connect() as db:
        query = (
            select(
                registers_date.c.start_service,
                registers_date.c.stop_service
            ).
            group_by(
                registers_date.c.start_service,
                registers_date.c.stop_service
            ).
            join(registers_date, registers_date.c.id == registers.c.registers_date_id_pk).
            where(
                and_(
                    registers.c.masters_id_pk == master_id,
                    extract('year', registers_date.c.start_service) == year,
                    extract('month', registers_date.c.start_service) == month
                )
            )
        )
        return db.execute(query).fetchall()


async def get_service(service_id: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                services.c.id,
                services.c.name,
                services.c.cost
            ).
            where(services.c.id == service_id)
        )
        return db.execute(query).fetchone()


async def get_service_data(category_id: int) -> dict:
    with engine.connect() as db:
        query = (
            select(
                services.c.id,
                services.c.name,
                services.c.time,
                services.c.cost
            ).
            where(services.c.categories_id_pk == category_id)
        )
        return db.execute(query).fetchall()


async def add_register(state: dict):
    date = datetime.strptime(state['date'], '%Y-%m-%d').date()
    start_time = datetime.strptime(state['start_time'], '%H:%M').time()
    stop_time = datetime.strptime(state['stop_time'], '%H:%M').time()

    master_id = state['master'][0]
    client_id = state['client'][1]
    client_table_id = state['client'][0]
    start = datetime.combine(date, start_time)
    stop = datetime.combine(date, stop_time)
    with engine.connect() as db:
        register_id = (
            insert(registers_date).
            values(
                start_service=start,
                stop_service=stop
            ).
            returning(registers_date.c.id)
        )
        register_id = db.execute(register_id).scalar()

        for service in state['services']:
            query = (
                insert(registers).
                values(
                    registers_date_id_pk=register_id,
                    masters_id_pk=master_id,
                    clients_id_pk=client_id,
                    client_table_id_pk=client_table_id,
                    service_id_pk=service[0]
                )
            )
            db.execute(query)
        db.commit()
