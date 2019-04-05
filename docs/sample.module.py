from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


class ModuleBasic():
    def __init__(self):
        self.name = "name"
        self.commands = ['command1', 'command2']

    def resolve_query(self, query):
        if query == "name-command":
            return self.command()

    def main_menu(self, bot, update):
        query = update.callback_query
        bot.edit_message_text(chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Commands",
            reply_markup=self.module_menu_keyboard())

    def get_commands_keyboard(self):
        keyboard = []
        for command in self.commands:
            keyboard.append(
                [InlineKeyboardButton(
                    '{}'.format(command),
                    callback_data='{}-{}'.format(
                    self.name, command))]
                )
        return keyboard

    def module_menu_keyboard(self):
        keyboard = self.get_commands_keyboard()
        return InlineKeyboardMarkup(keyboard)

    def callback_handler(self, bot, update):
        query = update.callback_query.data
        text = self.resolve_query(query)
        bot.send_message(
            text=text,
            chat_id=update.callback_query.message.chat.id
        )

    def command(self):
        print("hello world")
        return 100