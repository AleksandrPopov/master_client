class StartCommand:
    START = 'start'


class AccountCallback:
    ACCOUNT = 'account'
    CHANGE_NAME = f'{ACCOUNT}_name'
    CHANGE_CONTACT = f'{ACCOUNT}_phone'
    DELETE_ACCOUNT = f'{ACCOUNT}_delete'
    DELETE_CONFIRM = f'{ACCOUNT}_confirm'
    DELETE_CANCEL = f'{ACCOUNT}_cancel'
