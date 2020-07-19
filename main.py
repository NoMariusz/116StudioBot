import discord
from src.commands import *
from src.constants import *


class Discord116Bot:
    def __init__(self):
        self.client = discord.Client()
        self.token = self.get_token()

        @self.client.event
        async def on_message(message):
            print("BOT: get message '%s' by '%s'" % (message.content, message.author))

            for command in commands_dict.keys():
                if message.content.find(command) == 0:
                    if not commands_dict[command]["parametrized"]:
                        if command == str(message.content):
                            print("BOT: get command %s" % message.content)
                            await commands_dict[message.content]["command"](self.client, message)
                    else:
                        print("BOT: get command %s" % message.content)
                        await commands_dict[command]["command"](self.client, message)

    def run(self):
        self.client.run(self.token)

    @staticmethod
    def get_token():
        with open("data/token.txt", "r") as file:
            return file.read()


Discord116Bot().run()
