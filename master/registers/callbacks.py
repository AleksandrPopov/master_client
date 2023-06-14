from aiogram.utils.callback_data import CallbackData


class RegistersCallback:
    REGISTERS = 'registers'
    TIME = f'_time_{REGISTERS}'
    REGISTER = f'_reg_{REGISTERS}'
    DELETE = f'_delete{REGISTERS}'
    DELETE_CONFIRM = f'delete_confirm_{REGISTERS}'
    CANCEL = f'cancel_{REGISTERS}'
    BACK_TO_DATE = f'_back_to_date_{REGISTERS}'
    BACK_TO_TIME = f'_back_to_time_{REGISTERS}'

    REGISTERS_CALLBACK = CallbackData(f'calendar_{REGISTERS}', 'act', 'date', 'count', 'index', sep='|')
    NEXT_MONTH = 'NEXT_MONTH'
    PREV_MONTH = 'PREV_MONTH'
    DAY = 'DAY'
    IGNORE = f'IGNORE_{REGISTERS}'
