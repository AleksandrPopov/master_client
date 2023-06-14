class Command:
    REGISTERS = "Записи"


class Title:
    REGISTERS = f"<b>{Command.REGISTERS}</b>\n\n"
    REGISTER = "<b>Запис</b>\n\n"
    NEW_REGISTER = "<b>Новий запис</b>\n\n"
    ABORT_REGISTER = "<b>Запис скасовано</b>\n\n"


class Msg:
    DELETE_REGISTER = "Видалити?"
    NO_REGISTERS = "Намає записів"
    MASTER = "Майстер"
    CATEGORY = "Послуга"
    SERVICE = "Вид послуги"
    DATE = "Дата"
    TIME = "Час"
    CONTACT = "Телефон"
    NAME = "Ім'я"
    COST = "Ціна"


class Btn:
    YES = "Так"
    NO = "Ні"
    DELETE = "Видалити"
    BACK = "Назад"
    DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    MONTHS = ['0', 'Січень', 'Лютий', 'Березень', 'Квітень',
              'Травень', 'Червень', 'Липень', 'Серпень',
              'Вересень', 'Жовтень', 'Листопад', 'Грудень']
