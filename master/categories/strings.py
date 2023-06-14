class Command:
    CATEGORIES = "Послуги"


class Title:
    CATEGORIES = f"<b>{Command.CATEGORIES}</b>\n\n"


class Msg:
    ADD_CATEGORIES = "У Вас немає послуг"
    ENTER_CATEGORY_NAME = "Введіть назву послуги"
    ERROR_LONG_NAME = "Занадто довге ім'я"
    ERROR_EXISTS_NAME = "Послуга вже iснує"
    DELETE = "Видалити послугу?"


class Btn:
    YES = "Так"
    NO = "Ні"
    ADD = 'Додати'
    CHANGE_NAME = "Перейменувати"
    DELETE = "Видалити"
    BACK = "Назад"
