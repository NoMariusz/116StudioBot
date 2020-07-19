import json


class JsonHelper:

    @staticmethod
    def get_bot_data_dict():
        with open("data/bot_data.json", "r") as file:
            file_data = file.readline()
        return json.loads(file_data)

    @staticmethod
    def save_bot_data_dict(bot_dict: dict):
        with open("data/bot_data.json", "w") as file:
            file.write(str(json.dumps(bot_dict)))
