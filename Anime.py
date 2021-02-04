import json
import re
import requests
from bs4 import BeautifulSoup
import datetime
from myanimelist_utils import *


class Anime():

    def __init__(self, input):
        self.url = None
        self.id = None
        self.soup = None
        self.type = None
        self.name = None
        self.episodes = None
        self.status = None
        self.date_start = None
        self.date_end = None
        self.premiered = None
        self.producers = []
        self.licensors = []
        self.studios = []
        self.sources = None
        self.genres = []
        self.duration = None
        self.score = None
        self.ranked = None
        self.popularity = None
        self.members = None
        self.favorites = None
        self.relateds = {}
        self.total_duration = None
        self.time_between_episodes = None

        self.set_parameters(input)

    def __eq__(self, other):
        if isinstance(other, Anime):
            return self.id == other.id
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_parameters(self, input):
        self.url = self.set_url(input)
        self.id = self.set_id()
        if not self.soup: self.soup = self.set_soup()
        self.name = self.set_name()
        self.type = scrape_info(self.soup, "Type:")
        self.episodes = self.set_int("Episodes:")
        self.status = scrape_info(self.soup, "Status:")
        self.date_start, self.date_end = self.set_date()
        self.date_duration = self.date_end - self.date_start
        self.premiered = scrape_info(self.soup, "Premiered:")
        self.producers = scrape_info(self.soup, "Producers:").split(", ")
        self.licensors = scrape_info(self.soup, "Licensors:").split(", ")
        self.studios = scrape_info(self.soup, "Studios:").split(", ")
        self.sources = scrape_info(self.soup, "Source:")
        self.genres = scrape_info(self.soup, "Genres:").split(", ")  # TODO duplicate genre
        self.duration = self.set_duration()
        self.score = self.set_score()
        self.ranked = self.set_int("Ranked:")
        self.popularity = self.set_int("Popularity:")
        self.members = self.set_int("Members:")
        self.favorites = self.set_int("Favorites:")
        self.relateds = self.set_relateds()
        self.total_duration = self.duration * self.episodes
        self.time_between_episodes = self.set_time_between_episodes()

    def set_url(self, input):
        if re.match(r"^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime)\/([0-9]*)).*",
                    input):  # When manga "^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*"
            response = requests.get(input)
            if not response.ok:
                raise Exception(f"Invalid url in {self}, check that it's valid")
            else:
                html = response.text
                soup = BeautifulSoup(html, features="html.parser")
                self.soup = soup
                return parse_url(input)
        else:
            url = search(input, category="anime")
            return parse_url(url)

    def set_id(self):
        match = re.match(r"^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime)\/([0-9]*)).*",
                         self.url)  # When manga "^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*"
        return int(match.group(2))

    def set_soup(self):
        response = requests.get(self.url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        return soup

    def set_name(self):
        title = self.soup.find("h1", "title-name").find("strong").text
        return title

    def set_date(
            self):  # TODO There are animes with only the year such as https://myanimelist.net/anime/34878, it doesnt match and goes to the max date
        aired = scrape_info(self.soup, "Aired:")
        if match := re.match(r"^(\w{3} [0-9][0-9]?, [0-9]{4})(?: to (\w{3} [0-9][0-9]?, [0-9]{4})?)?", aired):
            date_start = datetime.datetime.strptime(match.group(1), '%b %d, %Y').date()

            if match.group(2):  # Only have start date, such as movies
                return date_start, datetime.datetime.strptime(match.group(2), '%b %d, %Y').date()

            return date_start, date_start
        return datetime.datetime.max.date(), datetime.datetime.max.date()

    def set_duration(self):
        scraped_duration = scrape_info(self.soup, "Duration:")
        duration = datetime.timedelta()
        value = 0
        if match := re.match(r"^([0-9][0-9]?) (hr|min|sec).? ?([0-9][0-9])? ?(hr|min|sec)?", scraped_duration):
            for i, group in enumerate(match.groups()):
                if group and i % 2 == 0:
                    value = int(group)
                elif group:
                    if group == "hr":
                        duration += datetime.timedelta(hours=value)
                    elif group == "min":
                        duration += datetime.timedelta(minutes=value)
                    elif group == "sec":
                        duration += datetime.timedelta(seconds=value)
                    value = 0
        return duration

    def set_int(self, info):
        scrapped = scrape_info(self.soup, info)
        parsed = scrapped.replace(",", "").replace("#", "")
        if parsed.isdigit():
            return int(parsed)
        return 0

    def set_score(self):
        scrapped_score = scrape_info(self.soup, "Score:")
        score = scrapped_score[:scrapped_score.find("(")].strip()
        try:
            return float(score)
        except:
            return 0

    def set_relateds(self):
        relateds = scrape_relateds(self.soup)
        return relateds

    def set_time_between_episodes(self):
        if self.episodes - 1 == 0: return datetime.timedelta(0)
        return (self.date_end - self.date_start) / (self.episodes - 1)

    def print_all_variables(self):
        attrs = vars(self)
        print('\n'.join(f"{key}: {value}" for key, value in attrs.items() if "soup" not in key))


if __name__ == "__main__":
    eva = Anime("Akira")
    eva.print_all_variables()
