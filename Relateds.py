import pickle
import sys
from time import sleep
from Anime import *
import operator


class Relateds():

    def __init__(self):
        self.first_anime = None
        self.old = []  # Already requested
        self.new = []  # To request
        self.removed = []  # User didn't want
        self.displayed = []

    def set_first(self, input):
        self.first_anime = Anime(input)
        self.new.append(self.first_anime)

    def add_anime(self, input):
        self.new.append(Anime(input))

    def next_step(self):
        temp = []
        current = self.new[:]
        for anime in current:
            relateds = anime.relateds
            for key, values in relateds.items():
                for value in values:
                    if all(anime.url != value for anime in self.old) and \
                            all(anime.url != value for anime in self.new) and \
                            all(anime.url != value for anime in self.removed) and \
                            re.match(r"^(?:https:\/\/|www.)?myanimelist\.net\/(anime|manga)\/[0-9]*.*", value).group(
                                1) != "manga":
                        new = Anime(value)
                        self.new.append(new)
                        print("Added", new.name)
            self.new.remove(anime)
            self.old.append(anime)
        self.new += temp

    def removed_remove(self, id):
        for anime in self.removed:
            if anime.id == id:
                self.removed.remove(anime)
                self.new.append(anime)
                return

    def removed_append(self, id):
        for anime in self.new:
            if anime.id == id:
                self.removed.append(anime)
                self.new.remove(anime)
                return

    def set_displayed(self):
        self.displayed = self.old + self.new
        self.displayed = [item for item in self.displayed if item not in self.removed]


if __name__ == "__main__":
    url = "Dragon Ball"
    relateds = Relateds()
    relateds.set_first(url)
    sys.setrecursionlimit(100000)

    while input("press: ") == "n":
        # while True:
        relateds.next_step()
        relateds.print_new()
        relateds.sort_sorted("date_start")
        # Store data (serialize)
