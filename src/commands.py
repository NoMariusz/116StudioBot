import discord
import datetime
from src.constants import *
from src.web_info_modul import WebInfoModul
from src.json_helper_modul import JsonHelper


async def make_help(client, message: discord.Message, **kwargs):
    help_embed = discord.Embed(title="Help for 116Studio Bot",
                               description="Help page have list of all commands and descriptions to it")
    for command, info in commands_dict.items():
        help_embed.add_field(name=command, value=info["description"])
    await message.channel.send(embed=help_embed)


async def on_stupki(client, message: discord.Message, **kwargs):
    await message.channel.send(":michalbie:")


async def display_michal_lol_time(client, message: discord.Message, **kwargs):
    bot_data = JsonHelper.get_bot_data_dict()
    time = WebInfoModul.get_user_lol_play_time("critovork")

    if "quiet" in kwargs.keys():
        if kwargs["quiet"]:
            return time

    hour_played_since_last_meeting = time - bot_data["last_meeting_michal_lol_hours_time"]
    time_since_last_meeting = datetime.datetime.now() - datetime.datetime.strptime(
        bot_data["last_meeting"], DATETIME_FORMAT)

    full_days_since_last_meeting = time_since_last_meeting.days
    part_days_since_last_meeting = time_since_last_meeting.seconds / 86400  # 86400 = 60 * 60 * 24 - how much seconds is in day
    days_since_last_meeting = full_days_since_last_meeting + part_days_since_last_meeting
    if days_since_last_meeting == 0:        # to not divide by 0
        days_since_last_meeting = 1 / 86400

    lol_hours_per_day = round(hour_played_since_last_meeting / days_since_last_meeting, 2)
    await message.channel.send(
        "Michał (critovork) :hot_face: :foot: has play in lol %s hours overall :thinking:\n and has play in lol %s hours"
        " from last meeting at %s\n this is %s hours per day :scream:"
        % (time, hour_played_since_last_meeting, bot_data["last_meeting"][:-9], lol_hours_per_day))
    return time


async def display_player_lol_time(client, message: discord.Message, **kwargs):
    command_len = 0
    if "command" in kwargs.keys():
        command_len = len(kwargs["command"]) + 1
    else:
        print("BOT: ERROR - parametrized command function not get 'command' arg")

    nick = str(message.content)[command_len:]
    time = WebInfoModul.get_user_lol_play_time(nick)
    if time is None:
        await message.channel.send("I can't find player %s :cry:" % nick)
    else:
        await message.channel.send(":video_game: %s played on lol %s hours overall :face_with_monocle: " % (nick, time))


async def set_next_meeting_date(client, message: discord.Message, **kwargs):
    command_len = 0
    if "command" in kwargs.keys():
        command_len = len(kwargs["command"]) + 1
    else:
        print("BOT: ERROR - parametrized command function not get 'command' arg")

    date_srt = str(message.content)[command_len:]
    try:
        datetime.datetime.strptime(date_srt, DATETIME_FORMAT)
    except Exception as ex:
        print("Commands: set_next_meeting_date() - Error\n %s" % ex)
        await message.channel.send("%s is in bad datetime format to set meeting datetime :dizzy_face:\n "
                                   "Correct format is %s" % (date_srt, DATETIME_FORMAT))
    else:
        data_dict = JsonHelper.get_bot_data_dict()
        data_dict["next_meeting"] = date_srt
        JsonHelper.save_bot_data_dict(data_dict)
        await message.channel.send("New meeting datetime %s was set :smirk:" % date_srt)
        await client.reload_meeting_event()


async def display_next_meeting_date(client, message: discord.Message, **kwargs):
    data_dict = JsonHelper.get_bot_data_dict()
    if data_dict["next_meeting"] is None:
        await message.channel.send("Next meeting date isn't set yet :frowning:")
    else:
        await message.channel.send("Next meeting is at %s in UTC :partying_face:" % data_dict["next_meeting"])


async def show_image_by_phrase(client, message: discord.Message, **kwargs):
    command_len = 0
    if "command" in kwargs.keys():
        command_len = len(kwargs["command"]) + 1
    else:
        print("BOT: ERROR - parametrized command function not get 'command' arg")
    phrase = str(message.content[command_len:])
    image_link = WebInfoModul.get_image_by_phrase(phrase)
    await message.channel.send("Here you go :cowboy: \n %s" % image_link)


async def show_random_image_by_phrase(client, message: discord.Message, **kwargs):
    command_len = 0
    if "command" in kwargs.keys():
        command_len = len(kwargs["command"]) + 1
    else:
        print("BOT: ERROR - parametrized command function not get 'command' arg")
    phrase = str(message.content[command_len:])
    image_link = WebInfoModul.get_image_by_phrase(phrase, random_=True)
    await message.channel.send("Here you go :cowboy: \n %s" % image_link)


async def on_dipon(client: discord.Client, message: discord.Message, **kwargs):
    last_msg = (await message.channel.history(limit=2).flatten())[1]
    emoji_names = ["🇩", "🇮", "🇵", "🇴", "🇳"]
    for emoji in emoji_names:
        await last_msg.add_reaction(emoji)
    await message.delete()


async def pin_word(client: discord.Client, message: discord.Message, **kwargs):
    print(message.guild)
    print(message.guild.emojis)
    command_len = 0
    if "command" in kwargs.keys():
        command_len = len(kwargs["command"]) + 1
    else:
        print("BOT: ERROR - parametrized command function not get 'command' arg")

    letter_to_emoji_translator = {chr(97 + x): chr(127462 + x) for x in range(0, 26)}
    last_msg = (await message.channel.history(limit=2).flatten())[1]
    word_to_translate = message.content.lower()[command_len:]

    is_external_emoji = False
    external_emoji = ""

    for letter in word_to_translate:
        if is_external_emoji:       # to pin server emojis
            external_emoji += letter
            if letter == ">":
                is_external_emoji = False
                try:
                    await last_msg.add_reaction(external_emoji)
                except Exception as e:
                    print("BOT: Error - %s" % e)
                external_emoji = ""
        elif letter in letter_to_emoji_translator.keys():
            try:
                await last_msg.add_reaction(letter_to_emoji_translator[letter])
            except discord.errors.Forbidden:
                break
        elif letter == "<": # to pin server emojis
            is_external_emoji = True
            external_emoji += letter
        else:
            try:  # to pin emoji's given in pin command
                await last_msg.add_reaction(letter)
            except discord.errors.HTTPException:
                print("BOT: pin_word() - can't translate symbol %s to letter emoji" % letter)
    await message.delete()


async def print_random_meme(client: discord.Client, message: discord.Message, **kwargs):
    meme_response = WebInfoModul.get_page_json_response("https://meme-api.herokuapp.com/gimme")
    while meme_response["nsfw"] or meme_response["spoiler"]:
        meme_response = WebInfoModul.get_page_json_response("https://meme-api.herokuapp.com/gimme")
    await message.channel.send("Go ahead! :laughing:\n %s" % meme_response["url"])

commands_dict = {
    COMMAND_BOT_SIGN + "stupka":
        {"description": "Display who like foots", "command": on_stupki, "parametrized": False},
    COMMAND_BOT_SIGN + "help":
        {"description": "Display help about bot", "command": make_help, "parametrized": False},
    COMMAND_BOT_SIGN + "michal_lol":
        {"description": "Display info about how much michal play lol", "command": display_michal_lol_time,
         "parametrized": False},
    COMMAND_BOT_SIGN + "played_lol":
        {"description": "Display info about how much given player play on lol", "command": display_player_lol_time,
         "parametrized": True},
    COMMAND_BOT_SIGN + "set_next_meeting":
        {"description": "Set date of next meeting, please use date in format %s\nRemember: set date in UTC time zone" % DATETIME_FORMAT,
         "command": set_next_meeting_date, "parametrized": True},
    COMMAND_BOT_SIGN + "next_meeting":
        {"description": "Display when is next meeting\nRemember: date should be in UTC time zone", "command": display_next_meeting_date,
         "parametrized": False},
    COMMAND_BOT_SIGN + "show":
        {"description": "Show first image at google search by given phrase", "command": show_image_by_phrase,
         "parametrized": True},
    COMMAND_BOT_SIGN + "showr":
        {"description": "Show random image from 20 first images at google search by given phrase", "command": show_random_image_by_phrase,
         "parametrized": True},
    COMMAND_BOT_SIGN + "dipon":
        {"description": "Pin word 'DIPON' by reactions in previous message on channel", "command": on_dipon,
         "parametrized": False},
    COMMAND_BOT_SIGN + "pin":
        {"description": "Pin given word to previous message by reactions\nRemember that letters in that word can't repeats !!!",
         "command": pin_word, "parametrized": True},
    COMMAND_BOT_SIGN + "meme":
        {"description": "Show for you random meme from reedit", "command": print_random_meme, "parametrized": False}
}
