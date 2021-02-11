import datetime
from myanimelist_utils import *


class Anime():

    def __init__(self, input):
        self.url = ""
        self.id = 0
        self.soup = None
        self.type = ""
        self.name = ""
        self.episodes = 0
        self.status = ""
        self.date_start = None
        self.date_end = None
        self.date_duration = None
        self.premiered = None
        self.producers = []
        self.licensors = []
        self.studios = []
        self.sources = ""
        self.genres = []
        self.duration = None
        self.score = 0
        self.ranked = 0
        self.popularity = 0
        self.members = 0
        self.favorites = 0
        self.relateds = {}
        self.watch_time = None
        self.time_between_episodes = None

        self._set_parameters(input)

    def __eq__(self, other):
        if isinstance(other, Anime):
            return self.id == other.id
        return False

    def __repr__(self):
        return self.name

    def _set_parameters(self, input):
        self.url = self._set_url(input)
        self.id = self._set_id()
        self.soup = self._set_soup()
        self.name = self._set_name()
        self.type = scrape_info(self.soup, "Type:")
        self.episodes = self._set_int("Episodes:")
        self.status = scrape_info(self.soup, "Status:")
        self.date_start, self.date_end = self._set_date()
        self.date_duration = self.date_end - self.date_start
        self.premiered = scrape_info(self.soup, "Premiered:")
        self.producers = scrape_info(self.soup, "Producers:").split(", ")
        self.licensors = scrape_info(self.soup, "Licensors:").split(", ")
        self.studios = scrape_info(self.soup, "Studios:").split(", ")
        self.sources = scrape_info(self.soup, "Source:")
        self.genres = self._set_genres()
        self.duration = self._set_duration()
        self.score = self._set_score()
        self.ranked = self._set_int("Ranked:")
        self.popularity = self._set_int("Popularity:")
        self.members = self._set_int("Members:")
        self.favorites = self._set_int("Favorites:")
        self.relateds = self._set_relateds()
        self.watch_time = self.duration * self.episodes
        self.time_between_episodes = self._set_time_between_episodes()

    def _set_url(self, input):
        if re.match(r"^((?:https://|www.)?myanimelist\.net/(?:anime)/([0-9]*)).*",
                    input):  # When manga "^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*"
            return parse_url(input)
        else:
            url = search(input, category="anime")
            return parse_url(url)

    def _set_id(self):
        match = re.match(r"^((?:https://|www.)?myanimelist\.net/(?:anime)/([0-9]*)).*",
                         self.url)  # When manga "^((?:https:\/\/|www.)?myanimelist\.net\/(?:anime|manga)\/([0-9]*)).*"
        return int(match.group(2))

    def _set_soup(self):
        response = requests.get(self.url)
        if not response.ok:
            raise Exception(f"Invalid url in {self}, check that it's valid")

        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        return soup

    def _set_name(self):
        title = self.soup.find("h1", "title-name").find("strong").text
        return title

    def _set_date(
            self):
        aired = scrape_info(self.soup, "Aired:")
        if match := re.match(r"^((\w{3} [0-9][0-9]?, )?[0-9]{4})(?: to (\w{3} [0-9][0-9]?, [0-9]{4})?)?", aired):
            if not match.group(2):  # Only year start
                date_start = datetime.datetime.strptime(match.group(1), '%Y').date()
            else:
                date_start = datetime.datetime.strptime(match.group(1), '%b %d, %Y').date()

            if match.group(3):  # Has end date
                return date_start, datetime.datetime.strptime(match.group(3), '%b %d, %Y').date()

            return date_start, date_start

        return datetime.datetime.max.date(), datetime.datetime.max.date()

    def _set_duration(self):
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

    def _set_int(self, info):
        scrapped = scrape_info(self.soup, info)
        parsed = scrapped.replace(",", "").replace("#", "")
        if parsed.isdigit():
            return int(parsed)
        return 0

    def _set_score(self):
        scrapped_score = scrape_info(self.soup, "Score:")
        score = scrapped_score[:scrapped_score.find("(")].strip()
        try:
            return float(score)
        except:
            return 0

    def _set_relateds(self):
        relateds = scrape_relateds(self.soup)
        return relateds

    def _set_time_between_episodes(self):
        if self.episodes - 1 == 0: return datetime.timedelta(0)
        return (self.date_end - self.date_start) / (self.episodes - 1)

    def _set_genres(self):
        text = scrape_info(self.soup, "Genres:")
        tmp = ""
        for idx, genre in enumerate(text.split(",")):
            genre = genre.strip()
            tmp += genre[:len(genre) // 2] + ", "
        text = tmp[:-2]
        return text.split(", ")

    def print_all_variables(self):
        attrs = vars(self)
        print('\n'.join(f"{key}: {value}" for key, value in attrs.items() if "soup" not in key))


if __name__ == "__main__":
    a = Anime("https://myanimelist.net/anime/34878")
    a.print_all_variables()
    b = Anime("https://myanimelist.net/anime/2222/Dr_Slump__Arale-chan")
    b.print_all_variables()

