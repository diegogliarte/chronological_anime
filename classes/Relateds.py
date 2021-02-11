import sys
from classes.Anime import *


class Relateds():

    def __init__(self):
        self.first_anime = None
        self.old = []  # Already requested
        self.new = []  # To request
        self.removed = []  # User didn't want
        self.pending_removed = [] # User will remove them once they hit next step
        self.displayed = [] # New + Old but not in Removed nor Pending Removed

    def set_first(self, input):
        self.first_anime = Anime(input)
        self.new.append(self.first_anime)

    def add_anime(self, input):
        self.new.append(Anime(input))

    def next_step(self):
        self.removed += self.pending_removed
        self.pending_removed = []
        temp = []
        self.new = [anime for anime in self.new if anime.url not in self.removed]
        current = self.new[:]
        for anime in current:
            relateds = anime.relateds
            for key, values in relateds.items():
                for value in values:
                    if all(anime.url != value for anime in self.old) and \
                            all(anime.url != value for anime in self.new) and \
                            all(url != value for url in self.removed) and \
                            re.match(r"^(?:https:\/\/|www.)?myanimelist\.net\/(anime|manga)\/[0-9]*.*", value).group(
                                1) != "manga":
                        new = Anime(value)
                        self.new.append(new)
                        print("Added", new.name)
            self.new.remove(anime)
            self.old.append(anime)
        self.new += temp

    def toggle_pending_remove(self, url):
        if url in self.pending_removed:
            self.pending_removed.remove(url)
        else:
            self.pending_removed.append(url)

    def set_displayed(self):
        self.displayed = self.old + self.new
        self.displayed = [item for item in self.displayed if item.url not in self.removed and item.url not in self.pending_removed]


if __name__ == "__main__":
    url = "Dragon Ball"
    relateds = Relateds()
    relateds.set_first(url)
    sys.setrecursionlimit(100000)

    while input("press: ") == "n":
        # while True:
        relateds.next_step()
        # Store data (serialize)
