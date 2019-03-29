import telegram

# def callback_handler(bot, update):
#     query = update.callback_query.data
#     text = core.get_response(query)
#     bot.send_message(
#         text=text,
#         chat_id=update.callback_query.message.chat.id
#     )


def start(bot, update):
    # keyboard = []
    # for module in core.modules:
    #     keyboard.append(
    #         telegram.KeyboardButton(
    #             "/{}".format(module)
    #         )
    #     )
    # reply_markup = telegram.ReplyKeyboardMarkup(
    #     utils.build_menu(
    #         keyboard,
    #         n_cols=len(keyboard)
    #     )
    # )
    bot.send_message(
        text="Welcome!",
        chat_id=update.message.chat_id
        # reply_markup=reply_markup
    )
