class CategoriesCallback:
    # Command and callback.
    CATEGORIES = 'categories'
    CATEGORIES_CALLBACK = '_C'

    # MENU: "Categories". BUTTONS: "*categories", "Add".
    ADD = f'add_category{CATEGORIES_CALLBACK}'
    MENU = f'menu{CATEGORIES_CALLBACK}'

    # MENU: "Menu category". BUTTONS: "Rename", "Delete", "Back".
    CHANGE = f'name_category{CATEGORIES_CALLBACK}'
    DELETE = f'delete_category{CATEGORIES_CALLBACK}'
    BACK = f'to_categories{CATEGORIES_CALLBACK}'

    # MENU: "Delete category". BUTTONS: "Yes", "No".
    DELETE_OK = f'delete_ok{CATEGORIES_CALLBACK}'
    DELETE_CANCEL = f'delete_cancel{CATEGORIES_CALLBACK}'
