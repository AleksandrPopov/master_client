class ServicesCallback:
    # Command and callback.
    SERVICES = 'services'
    SERVICES_CALLBACK = '_S'

    # MENU: "Services". BUTTONS: "*services", "Add", "Back".
    SERVICES_LIST = f'S{SERVICES_CALLBACK}'
    ADD_NAME = f'add_name{SERVICES_CALLBACK}'
    BACK_CATEGORIES = f'to_categories{SERVICES_CALLBACK}'
    ADD_SERVICE = f'add_service{SERVICES_CALLBACK}'

    # MENU: "Menu service". BUTTONS: "Rename", "Delete", "Cost", "Time", "Back".
    MENU = f'M{SERVICES_CALLBACK}'
    CHANGE_NAME = f'change_name{SERVICES_CALLBACK}'
    CHANGE_COST = f'change_cost{SERVICES_CALLBACK}'
    CHANGE_TIME = f'change_time{SERVICES_CALLBACK}'
    DELETE = f'delete_service{SERVICES_CALLBACK}'
    BACK_SERVICES = f'to_services{SERVICES_CALLBACK}'

    # MENU: "Delete category". BUTTONS: "Yes", "No".
    DELETE_OK = f'delete_ok{SERVICES_CALLBACK}'
    DELETE_CANCEL = f'delete_cancel{SERVICES_CALLBACK}'
