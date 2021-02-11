import requests
from bs4 import BeautifulSoup
import re


def search(name, category="anime"):
    url = f"https://myanimelist.net/{category}.php?q={name}"
    search_response = requests.get(url)
    search_html = search_response.text
    search_soup = BeautifulSoup(search_html, features="html.parser")
    first_entry = search_soup.find("div", "picSurround").find("a")
    return first_entry["href"]


def scrape_info(soup, info):
    try:
        vars = soup.find("span", "dark_text", text=re.compile(info))
        next = vars.next_sibling.strip()
        if next:
            text = next
        else:
            text = vars.parent.text.strip().replace(info, "")
            text = " ".join(text.split())

        return text
    except Exception as e:
        # print(e)
        return "Data not found"


def scrape_relateds(soup):
    category = None
    dict_relateds = {}
    table = soup.find("table", "anime_detail_related_anime")

    if table:
        relateds = table.find_all("td")

        for related in relateds:
            if hrefs := related.find_all("a"):
                for href in hrefs:
                    url = "https://myanimelist.net" + href["href"]
                    dict_relateds.setdefault(category, []).append(parse_url(url))
            else:
                category = related.text
    return dict_relateds

def scrape_user(user): # TODO complete user class and methods
    offset = 0
    json = get_user_json(user, offset)
    entries = []

    while (json and not "errors" in json):
        offset += 300
        entries += json
        json = get_user_json(user, offset)

    print("ENTRIES", entries)
    for idx, entry in enumerate(entries):
        print(idx, entry["anime_title"])

def get_user_json(user, offset):
    url = f"https://myanimelist.net/animelist/{user}/load.json?status=7&offset={offset}"
    request = requests.get(url)
    return request.json()


def parse_url(url):
    match = re.match(r"^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*", url)
    return match.group(1)


if __name__ == "__main__":
    # url = "https://myanimelist.net/anime/30/Neon_Genesis_Evangelion?q=evangelion&cat=anime"
    # response = requests.get(url)
    # html = response.text
    # soup = BeautifulSoup(html, features="html.parser")
    # print(scrape_info(soup, "Premiered:"))
    scrape_user("NexxBahamut")
