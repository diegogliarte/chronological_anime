from Anime import *
from Relateds import *
from operator import attrgetter
import math

def print_order_relateds(animes):
    i, j = 0, 1
    old = 1

    while i < len(animes) and j < len(animes):
        if is_date_inside(animes[j], animes[i]):
            difference = animes[j].date_start - animes[i].date_start
            between = 1 + difference / animes[i].time_between_episodes
            print(f"{animes[i]} ({old} - {math.floor(between)})")
            old = math.ceil(between)
            print(f"{animes[j]}")
            j += 1
        else:
            if old != 1:
                print(f"{animes[i]} ({old} - {animes[i].episodes})")
                old = 1
            else:
                print(f"{animes[i]}")

            i = j
            j += 1

    print(f"{animes[i]}")

def is_date_inside(insider:Anime, outsider:Anime):
    return insider.date_start > outsider.date_start and insider.date_end < outsider.date_end


if __name__ == "__main__":
    url = "Dragon Ball"
    relateds = Relateds()
    relateds.set_first(url)
    relateds.next_step()
    relateds.set_sorted()
    relateds.sort_sorted()
    print(relateds.sorted)
    print("\n\n")
    #animes = [Anime("Dragon Ball"), Anime("Dragon Ball Movie 1")]
    print_order_relateds(relateds.sorted)