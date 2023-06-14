from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from config import TZ
from client.add_register.callbacks import AddRegisterCallback
from client.add_register.parsers import exists_date
from client.add_register.strings import Btn

# Get client contact.
btn_get_contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_get_contact.insert(KeyboardButton(text=Btn.GET_CONTACT, request_contact=True))

btn_close = InlineKeyboardMarkup()
btn_close.insert(InlineKeyboardButton(text=Btn.OK, callback_data=AddRegisterCallback.OK))


# Masters list.
async def masters(masters_list: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)
    for master in masters_list:
        btn.insert(InlineKeyboardButton(
            text=master[1],
            callback_data=f'{master[0]}{AddRegisterCallback.CATEGORY}'
        ))
    return btn


# Categories list.
async def categories(categories_db: list, back: str = None) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)
    callback = dict(
        masters=AddRegisterCallback.BACK_TO_MASTERS,
        more_services=AddRegisterCallback.BACK_TO_MORE
    )
    for category in categories_db:
        btn.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=f'{category[0]}{AddRegisterCallback.SERVICE}')
        )
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.PRICE, callback_data=AddRegisterCallback.PRICE))

    if back is not None:
        btn.row()
        btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=callback.get(back)))

    return btn


# Services list.
async def services(services_db: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)

    for category in services_db:
        btn.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=f'{category[0]}{AddRegisterCallback.MORE}'))

    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=AddRegisterCallback.BACK_TO_CATEGORY))

    return btn


# Price.
async def price_list(callback: bool) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup()
    callback = AddRegisterCallback.SERVICE if callback else AddRegisterCallback.CATEGORY
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=callback))
    return btn


# Add more services.
async def more_services() -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text=Btn.NEXT, callback_data=AddRegisterCallback.DATE))
    btn.insert(InlineKeyboardButton(text=Btn.ADD, callback_data=AddRegisterCallback.CATEGORY))

    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=AddRegisterCallback.BACK_TO_SERVICE))
    return btn


# Date.
async def date(
        master_id: int,
        services_list: list,
        date_current: datetime.date = datetime.now(TZ).date()
) -> InlineKeyboardMarkup:
    calendar_days = await exists_date(
        master_id=master_id,
        date=date_current,
        services=services_list
    )

    btn = InlineKeyboardMarkup(row_width=7)
    callback = AddRegisterCallback.PREV_MONTH
    text = '<'

    # Short days name.
    btn.row()
    for days in Btn.DAYS:
        btn.insert(InlineKeyboardButton(
            text=days,
            callback_data=AddRegisterCallback.DATE_CALLBACK.new(AddRegisterCallback.IGNORE, date_current))
        )
    # Days.
    btn.row()
    for day in calendar_days:
        if day == 0:
            btn.insert(InlineKeyboardButton(
                text=" ",
                callback_data=AddRegisterCallback.DATE_CALLBACK.new(AddRegisterCallback.IGNORE, date_current))
            )
        else:
            btn.insert(InlineKeyboardButton(
                text=str(day),
                callback_data=f'{date_current.replace(day=day)}{AddRegisterCallback.TIME}'
            ))

    # Previous.
    btn.row()
    if datetime.now(TZ).month == date_current.month and datetime.now(TZ).year == date_current.year:
        text = ' '
        callback = AddRegisterCallback.IGNORE

    btn.insert(InlineKeyboardButton(
        text=text,
        callback_data=AddRegisterCallback.DATE_CALLBACK.new(callback, date_current))
    )

    # Month.
    btn.insert(InlineKeyboardButton(
        text=f'{Btn.MONTHS[date_current.month]} {date_current.year}',
        callback_data=AddRegisterCallback.DATE_CALLBACK.new(AddRegisterCallback.IGNORE, date_current))
    )

    # Next.
    btn.insert(InlineKeyboardButton(
        text=">",
        callback_data=AddRegisterCallback.DATE_CALLBACK.new(AddRegisterCallback.NEXT_MONTH, date_current))
    )

    # Back.
    btn.row()
    btn.insert(InlineKeyboardButton(
        text=Btn.BACK,
        callback_data=AddRegisterCallback.BACK_TO_MORE)
    )

    return btn


async def time(time_list: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=3)
    for hours in time_list:
        if hours != datetime.now().min:
            btn.insert(InlineKeyboardButton(
                text=hours.strftime('%H:%M'),
                callback_data=f'{hours.strftime("%H:%M")}{AddRegisterCallback.CONTACT}'
            ))
        else:
            btn.insert(InlineKeyboardButton(text=' ', callback_data=AddRegisterCallback.IGNORE))
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=AddRegisterCallback.BACK_TO_DATE))
    return btn


async def contacts(clients_list: list) -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)
    for client in clients_list:
        btn.row()
        btn.insert(InlineKeyboardButton(
            text=client[1],
            callback_data=f'{client[0]}{AddRegisterCallback.CONFIRM_REGISTER}'
        ))
    btn.row()
    btn.insert(InlineKeyboardButton(text=Btn.ADD, callback_data=AddRegisterCallback.ADD_CONTACT))
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=AddRegisterCallback.BACK_TO_TIME))
    return btn


async def confirm_register() -> InlineKeyboardMarkup:
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text=Btn.YES, callback_data=AddRegisterCallback.ADD_TO_DB))
    btn.insert(InlineKeyboardButton(text=Btn.BACK, callback_data=AddRegisterCallback.BACK_TO_CONTACT))
    return btn
