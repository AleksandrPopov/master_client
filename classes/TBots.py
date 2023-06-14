from contextlib import suppress

from aiogram import Bot, types
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted, MessageNotModified, \
    MessageToEditNotFound
from sqlalchemy import select, delete, and_, desc
from sqlalchemy.dialects.postgresql import insert

from database.connector import engine
from database.tables import messages


class TBot(Bot):
    def __init__(self, role: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__role = role

    async def add_messages(self, chat_id: int, message_id: int):
        with engine.connect() as db:
            db.execute(insert(messages).values(
                id=chat_id,
                role=self.__role,
                message_id=message_id + 1
            ))
            db.commit()

    async def get_messages(self, chat_id: int) -> list | bool:
        with engine.connect() as db:
            messages_db = db.execute(
                select(messages.c.message_id).
                where(
                    and_(
                        messages.c.id == chat_id,
                        messages.c.role == self.__role
                    )
                ).
                order_by(
                    desc(messages.c.message_id)
                )
            ).scalars().all()
            return messages_db

    async def del_messages(self, message: Message):
        with suppress(MessageToDeleteNotFound):
            await message.delete()

        d = await self.get_messages(chat_id=message.chat.id)
        r = self.__role

        for msg_id in d:
            with suppress(MessageToDeleteNotFound, MessageCantBeDeleted):
                t = await self.delete_message(chat_id=message.chat.id, message_id=msg_id)
                # print(types.Chat.)

            with engine.connect() as db:
                db.execute(
                    delete(messages).
                    where(
                        and_(
                            messages.c.id == message.chat.id,
                            messages.c.role == self.__role,
                            messages.c.message_id == msg_id,
                        )
                    )
                )
                db.commit()
        await self.add_messages(chat_id=message.chat.id, message_id=message.message_id)

    async def edit_messages(self, message: types.Message, text: str, btn: InlineKeyboardMarkup = None):
        messages_db = await self.get_messages(chat_id=message.chat.id)
        if messages_db is not None:
            with suppress(MessageToDeleteNotFound, MessageCantBeDeleted, MessageNotModified, MessageToEditNotFound):
                await message.delete()
                await self.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=messages_db[0],
                    text=text,
                    reply_markup=btn
                )

    async def edit_another_bot_message(self, chat_id: int, text: str):
        message_id = await self.get_messages(chat_id=chat_id)
        await self.send_message(chat_id=chat_id, text=text)
        if len(message_id) != 0:
            await self.add_messages(chat_id=chat_id, message_id=message_id[0])
