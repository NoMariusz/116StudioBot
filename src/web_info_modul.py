from bs4 import BeautifulSoup
import requests


class WebInfoModul:

    @staticmethod
    def get_user_lol_play_time(username: str):
        page = requests.get("https://wol.gg/stats/eune/%s/" % username.lower().replace(" ", ""))
        pagebs = BeautifulSoup(page.content, "html.parser")
        try:
            play_count_div = pagebs.find("div", id="time-hours")
            play_count = int(play_count_div.find("p").getText()[:-5].replace(",", ""))
            print("WebInfoModul: get_user_lol_play_time() - username: %s, play_count: %s" % (username, play_count))
            return play_count
        except AttributeError as e:
            print("WebInfoModul: error\n %s" % e)
            return None
