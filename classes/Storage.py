import json
import typing
from aiogram.contrib.fsm_storage.memory import BaseStorage
from sqlalchemy import select, delete, and_, update
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import states


class BotStorage(BaseStorage):

    def __init__(self, role: str):
        self.role = role

    async def set_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        state: typing.Optional[typing.AnyStr] = None):
        with engine.connect() as db:
            db.execute(insert(states)
                       .values(user=user, chat=chat, role=self.role, state=state)
                       .on_conflict_do_update(constraint=states.primary_key, set_=dict(state=state)))
            db.commit()

    async def get_state(self, *,
                        chat: typing.Union[str, int, None] = None,
                        user: typing.Union[str, int, None] = None,
                        default: typing.Optional[str] = None) -> typing.Optional[str]:
        with engine.connect() as db:
            query = (
                select(states.c.state).
                where(
                    states.c.user == user,
                    states.c.chat == chat,
                    states.c.role == self.role
                )
            )
            return db.execute(query).scalar()

    async def set_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):
        pass

    async def get_data(self, *,
                       chat: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       default: typing.Optional[typing.Dict] = None) -> typing.Dict:
        with engine.connect() as db:
            query = (
                select(states.c.data).
                where(
                    states.c.user == user,
                    states.c.chat == chat,
                    states.c.role == self.role
                )
            )
            query = db.execute(query).scalar()
            return query if query is not None else {}

    async def update_data(self, *,
                          chat: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None,
                          **kwargs):
        with engine.connect() as db:
            db.execute(
                insert(states).
                values(user=user, chat=chat, role=self.role, data=kwargs).
                on_conflict_do_update(
                    constraint=states.primary_key,
                    set_=dict(data=states.c.data + json.dumps(kwargs)),
                    where=and_(
                        states.c.user == user,
                        states.c.chat == chat,
                        states.c.role == self.role
                    )
                )
            )
            db.commit()

    async def reset_state(self, *,
                          chat: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          with_data: typing.Optional[bool] = True):
        with engine.connect() as db:
            if with_data:
                db.execute(
                    delete(states).
                    where(and_(states.c.user == user, states.c.chat == chat))
                )
                db.commit()
            else:
                db.execute(
                    update(states).
                    where(and_(states.c.user == user, states.c.chat == chat)).
                    values(state=None)
                )
                db.commit()

    async def add_messages(self):
        pass

    async def finish(self, *,
                     chat: typing.Union[str, int, None] = None,
                     user: typing.Union[str, int, None] = None):
        with engine.connect() as db:
            db.execute(
                delete(states).
                where(states.c.user == user and states.c.chat == chat)
            )
            db.commit()

    async def set_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         bucket: typing.Dict = None):
        pass

    async def get_bucket(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                         default: typing.Optional[dict] = None) -> typing.Dict:
        pass

    async def update_bucket(self, *, chat: typing.Union[str, int, None] = None,
                            user: typing.Union[str, int, None] = None, bucket: typing.Dict = None, **kwargs):
        pass

    async def wait_closed(self):
        pass

    async def close(self):
        pass
