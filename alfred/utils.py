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


def get_extension_keyboards():
    keyboard = []
    for dict in config.extensions:
        if dict['active']:
            keyboard.append(
                [InlineKeyboardButton(
                    '{}'.format(dict['name']),
                    callback_data='{}-main'.format(dict['name'].lower()))]
            )
    return keyboard
