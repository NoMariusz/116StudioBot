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

            if message.content in commands_dict.keys():
                print("BOT: get command %s" % message.content)
                await commands_dict[message.content]["command"](self.client, message)

            elif message.content == COMMAND_BOT_SIGN + "help":
                help_embed = discord.Embed(title="Help for 116 Studio Bot",
                                           description="Help page have list of all commands and descriptions to it")
                for command, info in commands_dict.items():
                    help_embed.add_field(name=command, value=info["description"])
                await message.channel.send(embed=help_embed)

    def run(self):
        self.client.run(self.token)

    @staticmethod
    def get_token():
        with open("data/token.txt", "r") as file:
            return file.read()


Discord116Bot().run()
