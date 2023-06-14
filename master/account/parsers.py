import phonenumbers

from master.account.strings import Msg


async def format_contact(contact: str, country: str) -> str | bool:
    if contact[1:].isdigit() and phonenumbers.is_valid_number(phonenumbers.parse(contact, country)):
        return phonenumbers.format_number(phonenumbers.parse(contact, country), phonenumbers.PhoneNumberFormat.E164)
    else:
        return False


async def msg_builder(name: str, contact: str) -> str:
    len_max = max([len(Msg.NAME), len(Msg.CONTACT)])

    res_name = " " * (len_max - len(Msg.NAME) + 3)
    res_contact = " " * (len_max - len(Msg.CONTACT) + 3)

    return f"<code>{Msg.NAME}:{res_name}</code>{name}\n" \
           f"<code>{Msg.CONTACT}:{res_contact}</code>{contact}\n"
