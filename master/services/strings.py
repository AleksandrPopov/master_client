class Command:
    SERVICES = "Види послуг"


class Title:
    SERVICES = f"<b>{Command.SERVICES}</b>\n\n"


class Msg:
    NOT_EXISTS_CATEGORIES = "У Вас немає послуг"
    NOT_EXISTS_SERVICES = "У Вас немає видiв послуг"
    EXISTS_SERVICES = "Вид послуги вже iснує"
    ENTER_SERVICE_NAME = "Введіть назву виду послуг"
    ERROR_NAME = "Занадто довге ім'я"
    ENTER_TIME = "Введіть час у хвилинах"
    ERROR_TIME = "Не правильно вказаний час. Введіть число"
    ERROR_COST = "Не правильно вказана вартість. Введіть число"

    ADD_SERVICE = "Додайте вид послуг"
    SERVICES = "Види послуг"
    DELETE = "Видалити вид послуги?"
    ENTER_NAME = "Введіть нове ім'я"
    ENTER_COST = "Введіть вартість"

    ERROR_TIME_LEN = "Введіть час, не більше 3-х символів"
    ERROR_COST_LEN = "Введіть вартість, не більше 10-ти символів"

    TIME = "Час"
    NAME = "Ім'я"
    COST = "Вартість"
    UAH = "грн."
    MINUTES = "хв."
    HOUR = "г."


class Btn:
    YES = "Так"
    NO = "Ні"
    ADD = 'Додати'
    SERVICES = "Види послуг"
    CHANGE_NAME = "Перейменувати"
    DELETE = "Видалити"
    TIME = "Час"
    COST = "Вартість"
    BACK = "Назад"
