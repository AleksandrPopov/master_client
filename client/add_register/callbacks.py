from aiogram.utils.callback_data import CallbackData


class AddRegisterCallback:
    START = 'start'
    ADD_REGISTER = '_add_reg'
    DATE_CALLBACK = CallbackData(f'_date_call{ADD_REGISTER}', 'act', 'date', sep='|')

    PRICE = f'_price{ADD_REGISTER}'
    CATEGORY = f'_category{ADD_REGISTER}'
    SERVICE = f'_service{ADD_REGISTER}'
    MORE = f'_more{ADD_REGISTER}'
    DATE = f'_date{ADD_REGISTER}'
    TIME = f'_time{ADD_REGISTER}'
    ADD_CONTACT = f'_add_cont{ADD_REGISTER}'
    CONTACT = f'_contact{ADD_REGISTER}'
    CONFIRM_REGISTER = f'_confirm_register{ADD_REGISTER}'
    ADD_TO_DB = f'_add_to_db{ADD_REGISTER}'
    OK = f'_ok{ADD_REGISTER}'

    # Date
    DAY = 'DAY'
    NEXT_MONTH = 'NEXT_MONTH'
    PREV_MONTH = 'PREV_MONTH'
    IGNORE = 'IGNORE'

    BACK_TO_MASTERS = f'_master{ADD_REGISTER}'
    BACK_TO_CATEGORY = f'_back_to_cat{ADD_REGISTER}'
    BACK_TO_SERVICE = f'_back_to_ser{ADD_REGISTER}'
    BACK_TO_MORE = f'_back_to_mor{ADD_REGISTER}'
    BACK_TO_DATE = f'_back_to_dat{ADD_REGISTER}'
    BACK_TO_TIME = f'_back_to_tim{ADD_REGISTER}'
    BACK_TO_CONTACT = f'_back_to_cont{ADD_REGISTER}'

