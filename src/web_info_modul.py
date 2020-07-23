from bs4 import BeautifulSoup
import requests
import urllib.parse
import random


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

    @staticmethod
    def get_image_by_phrase(phrase: str, random_=False):
        print("WebInfoModul: get_random_image_by_phrase() - get phrase %s" % phrase)
        phrase = urllib.parse.quote(phrase)
        page = requests.get(
            "https://www.google.com/search?q=%s&client=firefox-b-d&sxsrf=ALeKk02MPCjTXSzZSvqA2w2E4cbJ_ZWQSw:1595361162486&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi_hIO7j9_qAhVVSxUIHcDKAsUQ_AUoAXoECB0QAw" % phrase)
        pagebs = BeautifulSoup(page.content, "html.parser")
        images_links = []

        if not random_:
            return pagebs.find(class_="RAyV4b").img["src"]

        for elem in pagebs.find_all(class_="RAyV4b"):
            link = elem.img["src"]
            images_links.append(link)
        if not images_links:
            print("WebInfoModul: get_random_image_by_phrase() - can not find any image in requested page")
        return random.choice(images_links)

    @staticmethod
    def get_page_json_response(link: str):
        page = requests.get(link)
        return page.json()


