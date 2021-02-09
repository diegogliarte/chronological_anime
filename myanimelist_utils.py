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
            text = vars.parent.text.strip().replace(info, "") # TODO See if al this can be done nicer
            text = " ".join(text.split())
            if info == "Genres:":
                temp = ""
                for idx, genre in enumerate(text.split(",")):
                    genre = genre.strip()
                    temp += genre[:len(genre)//2] + ", "
                text = temp[:-2]

        return text
    except Exception as e:
        # print(e)
        return "Scraper failed, data not found"


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


def parse_url(url):
    match = re.match(r"^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*", url)
    return match.group(1)


if __name__ == "__main__":
    url = "https://myanimelist.net/anime/30/Neon_Genesis_Evangelion?q=evangelion&cat=anime"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="html.parser")
    print(scrape_info(soup, "Premiered:"))
