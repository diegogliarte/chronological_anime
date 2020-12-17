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
        self.sorted = []
        self.reversed = False
        self.timeline = []

    def set_first(self, input):
        self.first_anime = Anime(input)
        self.new.append(self.first_anime)

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

    def set_sorted(self):
        self.sorted = self.old + self.new
        self.sorted = [item for item in self.sorted if item not in self.removed]

    def sort_sorted(self, attribute="date_start"):
        keyfun = operator.attrgetter(attribute)
        self.sorted.sort(key=keyfun, reverse=self.reversed)

    def sort_reverse(self):
        self.reversed = not self.reversed

    def set_timeline(self):
        for anime in self.sorted:
            anime_dict = {"name": anime.name, "type": anime.type,"date_start": anime.date_start.strftime("%Y %m %d"), "date_end": anime.date_end.strftime("%Y %m %d"),}
            self.timeline.append(anime_dict)


    def print_old(self):
        print("\nOld")
        for i in self.old:
            print(i.name)
        print()

    def print_removed(self):
        print("\nRemoved")
        for i in self.removed:
            print(i.name)
        print()

    def print_new(self):
        print("\nNew")
        for i in self.new:
            print(i.name)
        print()


if __name__ == "__main__":
    url = "FLCL"
    relateds_obj = Relateds()
    relateds_obj.set_first(url)
    sys.setrecursionlimit(100000)

    while input("press: ") == "n":
        # while True:
        relateds_obj.next_step()
        relateds_obj.print_new()
        relateds_obj.sort_sorted("date_start")
        # Store data (serialize)