import discord
import datetime
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

    hour_played_since_last_meeting = time - bot_data["last_meeting_michal_lol_hours_time"]
    time_since_last_meeting = datetime.datetime.now() - datetime.datetime.strptime(bot_data["last_meeting"], DATETIME_FORMAT)
    days_since_last_meeting = time_since_last_meeting.days if time_since_last_meeting.days != 0 else 1
    lol_hours_per_day = hour_played_since_last_meeting / days_since_last_meeting
    await message.channel.send("Michał (critovork) has play in lol %s hours overall\n and has play in lol %s hours from last meeting at %s\n this is %s hours per day"
                               % (time, hour_played_since_last_meeting, bot_data["last_meeting"][:-9], lol_hours_per_day))


async def display_player_lol_time(client: discord.Client, message: discord.Message):
    nick = str(message.content)[12:]
    time = WebInfoModul.get_user_lol_play_time(nick)
    if time is None:
        await message.channel.send("I can't find player %s" % nick)
    else:
        await message.channel.send("%s played on lol %s hours overall" % (nick, time))


async def set_next_meeting_date(client: discord.Client, message: discord.Message):
    date_srt = str(message.content)[18:]
    try:
        datetime.datetime.strptime(date_srt, DATETIME_FORMAT)
    except Exception as ex:
        print("Commands: set_next_meeting_date() - Error\n %s" % ex)
        await message.channel.send("%s is in bad datetime format to set meeting datetime\n Correct format is %s" % (date_srt, DATETIME_FORMAT))
    else:
        data_dict = JsonHelper.get_bot_data_dict()
        data_dict["next_meeting"] = date_srt
        JsonHelper.save_bot_data_dict(data_dict)
        await message.channel.send("New meeting datetime %s was set" % date_srt)


async def display_next_meeting_date(client: discord.Client, message: discord.Message):
    data_dict = JsonHelper.get_bot_data_dict()
    await message.channel.send("Next meeting is at %s" % data_dict["next_meeting"])


commands_dict = {
    COMMAND_BOT_SIGN + "stupka": {"description": "Say wjo like foots", "command": on_stupki, "parametrized": False},
    COMMAND_BOT_SIGN + "help": {"description": "Display help about bot", "command": make_help, "parametrized": False},
    COMMAND_BOT_SIGN + "michal_lol": {"description": "Display info about how much michal play lol", "command": display_michal_lol_time, "parametrized": False},
    COMMAND_BOT_SIGN + "played_lol": {"description": "Display info about how much given player play on lol", "command": display_player_lol_time, "parametrized": True},
    COMMAND_BOT_SIGN + "set_next_meeting": {"description": "Set date of next meeting, please use date in format %s" % DATETIME_FORMAT, "command": set_next_meeting_date, "parametrized": True},
    COMMAND_BOT_SIGN + "next_meeting": {"description": "Display when is next meeting", "command": display_next_meeting_date, "parametrized": False}
}
