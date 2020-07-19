from bs4 import BeautifulSoup
import requests


class WebInfoModul:

    @staticmethod
    def get_user_lol_play_time(username: str):
        page = requests.get("https://wol.gg/stats/eune/%s/" % username.lower())
        pagebs = BeautifulSoup(page.content, "html.parser")
        play_count_div = pagebs.find("div", id="time-hours")
        play_count = int(play_count_div.find("p").getText()[:-5].replace(",", ""))
        print("WebInfoModul: get_user_lol_play_time() - play_count_div: %s, play_count: %s" % (play_count_div, play_count))
        return play_count
