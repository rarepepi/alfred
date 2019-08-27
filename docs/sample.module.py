class Module(AlfredModule):
    def __init__(self):
        self.name = "mod_name"
        self.menu_name = "📟 Pretty Mod Name"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]

    def get_balance_detailed(self):
        return "Anything you want"
