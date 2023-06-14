from aiogram.utils.callback_data import CallbackData

from master.schedules.strings import Btn


class SchedulesCallback:
    SCHEDULES = "schedules"
    SCHEDULES_CALLBACK = CallbackData(SCHEDULES, 'act', 'start', 'stop', 'day', sep='|')
    IGNORE = "IGNORE"

    # MENU: "Confirm choice schedule and choice day off". BUTTONS: "Add", "Day off",
    ADD = "ADD"
    DAY_OFF = "DAYS_OFF"

    # MENU: "Choice of start time". BUTTONS: "Up hour", "Up minutes", "Down hour", "Down minutes".
    START_UP_HOUR = "SUH"
    START_UP_MIN = "SUM"
    STOP_UP_HOUR = "EUH"
    STOP_UP_MIN = "EUM"

    # MENU: "Choice of end time". BUTTONS: "Up hour", "Up minutes", "Down hour", "Down minutes".
    START_DOWN_HOUR = "SDH"
    START_DOWN_MIN = "SDM"
    STOP_DOWN_HOUR = "EDH"
    STOP_DOWN_MIN = "EDM"

    # Callbacks lists for buttons.
    row_1 = ((Btn.UP, START_UP_HOUR), (Btn.UP, START_UP_MIN),
             (Btn.EMPTY, IGNORE), (Btn.UP, STOP_UP_HOUR), (Btn.UP, STOP_UP_MIN))

    row_2 = ((Btn.EMPTY, IGNORE), (Btn.EMPTY, IGNORE), (Btn.EMPTY, IGNORE), (Btn.DASH, IGNORE), (Btn.EMPTY, IGNORE))

    row_3 = ((Btn.DOWN, START_DOWN_HOUR), (Btn.DOWN, START_DOWN_MIN),
             (Btn.EMPTY, IGNORE), (Btn.DOWN, STOP_DOWN_HOUR), (Btn.DOWN, STOP_DOWN_MIN))
