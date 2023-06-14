from aiogram.utils.callback_data import CallbackData


class DaysOffCallback:
    DAYS_OFF = 'days_off'
    DAYS_OFF_CALLBACK = CallbackData(DAYS_OFF, 'act', 'date', 'days_off', sep='|')
    SELECT = 'DS'
    IGNORE = 'IGNORE'
    ADD = 'ADD'
    DELETE = 'DELETE'
    DELETE_CONFIRM = 'DELETE_CONFIRM'
    CANCEL = 'CANCEL'
    NEXT_MONTH = 'NEXT_MONTH'
    PREV_MONTH = 'PREV_MONTH'
    SELECT_DAY = 'SELECT_DAY'
    CLEAR = 'CLEAR'

