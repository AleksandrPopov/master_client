class Command:
    SCHEDULES = "Режим роботи"


class Title:
    SCHEDULES = f"<b>{Command.SCHEDULES}</b>\n\n"


class Msg:
    SCHEDULES = "<i>1. Оберіть день, для якого потрібно встановити режим роботи.</i>\n" \
                "<i>2. Встановіть час початку та кінця робочого дня, або виберіть Вихідний.</i>\n" \
                "<i>3. Натисніть кнопку Додати.</i>\n" \
                "<i>4. Повторіть пункти 1-3 для інших днів тижня, що залишилися.</i>\n"


class Btn:
    EMPTY = ' '
    DASH = '---'
    UP = '↑'
    DOWN = '↓'
    ADD = 'Додати'
    DAY_OFF = 'Вихідний'
    DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    DAYS_LONG = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота', 'Неділя']
    DAY_OFF_SCHEDULE = "00:00 - 00:00"
