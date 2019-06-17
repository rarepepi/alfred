import config
from telegram import (
    InlineKeyboardButton
)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def get_menus_of_active_modules():
    keyboard = []
    active = [mod for mod in config.modules if mod['active']]
    for mod in active:
        keyboard.append(
            [InlineKeyboardButton(
                '{}'.format(mod['name']),
                callback_data=f"{mod['name'].lower()}-main")]
        )
    return keyboard
