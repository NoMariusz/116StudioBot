import discord
from src.constants import *


async def make_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Help for 116 Studio Bot",
                               description="Help page have list of all commands and descriptions to it")
    for command, info in commands_dict.items():
        help_embed.add_field(name=command, value=info["description"])
    await message.channel.send(embed=help_embed)


async def on_stupki(client: discord.Client, message: discord.Message):
    await message.channel.send("Michał")

commands_dict = {
    COMMAND_BOT_SIGN + "stupka": {"description": "Say about man who like stupka's", "command": on_stupki, "parametrized": False},
    COMMAND_BOT_SIGN + "help": {"description": "Display help about bot", "command": make_help, "parametrized": False}
}
