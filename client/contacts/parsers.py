from client.contacts.strings import Msg


async def contact_msg_builder(contact_data: dict = None) -> str:
    name, contact = '-', '-'
    len_max = max([len(Msg.NAME), len(Msg.CONTACT)])
    name_len = " " * (len_max - len(Msg.NAME) + 3)
    contact_len = " " * (len_max - len(Msg.CONTACT) + 3)

    if contact_data is not None:
        name = contact_data[1]
        contact = contact_data[2]

    return f"<code>{Msg.NAME}:{name_len}</code><b>{name}</b>\n" \
           f"<code>{Msg.CONTACT}:{contact_len}</code><b>{contact}</b>\n"
