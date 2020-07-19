import discord
from src.constants import *
from src.web_info_modul import WebInfoModul
from src.json_helper_modul import JsonHelper


async def make_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Help for 116 Studio Bot",
                               description="Help page have list of all commands and descriptions to it")
    for command, info in commands_dict.items():
        help_embed.add_field(name=command, value=info["description"])
    await message.channel.send(embed=help_embed)


async def on_stupki(client: discord.Client, message: discord.Message):
    await message.channel.send("Michał")


async def display_michal_lol_time(client: discord.Client, message: discord.Message):
    bot_data = JsonHelper.get_bot_data_dict()
    time = WebInfoModul.get_user_lol_play_time("critovork")
    await message.channel.send("Michał (critovork) has play in lol %s hours overall" % time)
    await message.channel.send("Michał (critovork) has play in lol %s hours from last meeting at %s"
                               % (time - bot_data["last_meeting_michal_lol_hours_time"], bot_data["last_meeting"]))

commands_dict = {
    COMMAND_BOT_SIGN + "stupka": {"description": "Say about man who like stupka's", "command": on_stupki, "parametrized": False},
    COMMAND_BOT_SIGN + "help": {"description": "Display help about bot", "command": make_help, "parametrized": False},
    COMMAND_BOT_SIGN + "michal_lol": {"description": "Display info about how much michal play lol", "command": display_michal_lol_time, "parametrized": False}
}
