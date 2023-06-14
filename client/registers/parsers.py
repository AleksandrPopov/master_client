from country_currencies import get_by_country

from config import COUNTRY
from client.registers.strings import Msg


async def registers_msg_builder(register: dict) -> str:

    len_max = max(
        [len(Msg.MASTER),
         len(Msg.CATEGORY),
         len(Msg.SERVICE),
         len(Msg.DATE),
         len(Msg.TIME),
         len(Msg.CONTACT),
         len(Msg.NAME),
         len(Msg.COST)])

    len_master = " " * (len_max - len(Msg.MASTER) + 3)
    len_category = " " * (len_max - len(Msg.CATEGORY) + 3)
    len_service = " " * (len_max - len(Msg.SERVICE) + 3)
    len_date = " " * (len_max - len(Msg.DATE) + 3)
    len_time = " " * (len_max - len(Msg.TIME) + 3)
    len_contact = " " * (len_max - len(Msg.CONTACT) + 3)
    len_name = " " * (len_max - len(Msg.NAME) + 3)
    len_cost = " " * (len_max - len(Msg.COST) + 3)

    return f"<code>{Msg.MASTER}:{len_master}</code>{register[2]}\n" \
           f"<code>{Msg.CATEGORY}:{len_category}</code>{register[5]}\n" \
           f"<code>{Msg.SERVICE}:{len_service}</code>{register[6]}\n" \
           f"<code>{Msg.COST}:{len_cost}</code>{register[7]} {get_by_country(COUNTRY)[0]}\n" \
           f"<code>{Msg.DATE}:{len_date}</code>{register[8].date().strftime('%d.%m.%Y')}\n" \
           f"<code>{Msg.TIME}:{len_time}</code>{register[8].time().strftime('%H:%M')} - {register[9].time().strftime('%H:%M')}\n" \
           f"<code>{Msg.NAME}:{len_name}</code>{register[3]}\n" \
           f"<code>{Msg.CONTACT}:{len_contact}</code>{register[4]}\n"
