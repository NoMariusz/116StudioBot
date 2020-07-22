import discord
import asyncio
from src.commands import *
from src.json_helper_modul import JsonHelper


class Discord116Bot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.token = self.get_token()
        self.meeting_event = None

    async def on_message(self, message):
        print("BOT: get message '%s' by '%s'" % (message.content, message.author))

        for command in commands_dict.keys():
            if message.content.find(command) == 0:      # to activate command when message starts with it
                if not commands_dict[command]["parametrized"]:
                    if command == str(message.content):
                        print("BOT: get command %s" % message.content)
                        await commands_dict[message.content]["command"](self, message)
                elif str(message.content)[len(command)] == " ":   # to not activate command which name is sub-name other
                    print("BOT: get command %s" % message.content)
                    await commands_dict[command]["command"](self, message, command=command)

    async def on_ready(self):
        print("BOT: ready")
        await self.init_meeting_event()

    def run(self, *args, **kwargs):
        super().run(self.token)

    @staticmethod
    def get_token():
        with open("data/token.txt", "r") as file:
            return file.read()

    async def init_meeting_event(self):
        if JsonHelper.get_bot_data_dict()["next_meeting"] is not None:
            self.meeting_event = asyncio.create_task(self.made_meeting_event())
            await self.meeting_event
        else:
            print("BOT: init_meeting_event() - meeting date null")

    async def made_meeting_event(self):
        meeting_date_str = JsonHelper.get_bot_data_dict()["next_meeting"]
        meeting_date = datetime.datetime.strptime(meeting_date_str, DATETIME_FORMAT)
        now_date = datetime.datetime.now().utcnow()
        time_to_meeting = meeting_date - now_date
        print("BOT: made_meeting_event() - time to meeting %s" % time_to_meeting)
        await discord.utils.sleep_until(meeting_date)
        print("BOT: made_meeting_event() - meeting going to start")
        await self.on_meeting_start()

    async def on_meeting_start(self):
        print("BOT: on_meeting_start()")
        send_message = None
        for channel in self.get_all_channels():
            if channel.name == "bot":
                print("BOT: meeting start")
                send_message = await channel.send("@everyone 116 Studio meeting stared !!! :kissing_heart:")
                await channel.send(":heart: :heart: :heart: Good Luck :heart: :heart: :heart:")
                break
        else:
            print("BOT: ERROR meeting start - not find bot channel")

        bot_data_dict = JsonHelper.get_bot_data_dict()
        bot_data_dict["last_meeting"] = bot_data_dict["next_meeting"]
        bot_data_dict["next_meeting"] = None
        if send_message is None:
            time = await display_michal_lol_time(self, message=send_message, quiet=True)
        else:
            time = await display_michal_lol_time(self, message=send_message)
        bot_data_dict["last_meeting_michal_lol_hours_time"] = time
        print("BOT: meeting_event_start - new bot_data_dict: %s" % bot_data_dict)
        JsonHelper.save_bot_data_dict(bot_data_dict)

        self.meeting_event = None

    async def reload_meeting_event(self):
        if self.meeting_event is not None:
            self.meeting_event.cancel()
        print("BOT: reload_meeting_event() - cancel meeting event")
        await self.init_meeting_event()


Discord116Bot().run()
