from Anime import *
from Relateds import *
from operator import attrgetter
import math

def order_relateds(animes):
    animes = sorted(animes, key=lambda anime: anime.date_start)
    message = ""
    i, j = 0, 1
    old = 1

    while i < len(animes) and j < len(animes):
        if is_date_inside(animes[j], animes[i]):
            difference = animes[j].date_start - animes[i].date_start
            between = 1 + difference / animes[i].time_between_episodes
            message += f"{animes[i]} ({old} - {math.floor(between)})\n"
            old = math.ceil(between)
            message += f"{animes[j]}\n"
            j += 1
        else:
            if old != 1:
                message += f"{animes[i]} ({old} - {animes[i].episodes})\n"
                old = 1
            else:
                message += f"{animes[i]}\n"

            i = j
            j += 1

    if old != 1:
        message += f"{animes[i]} ({old} - {animes[i].episodes})\n"
    else:
        message += f"{animes[i]}"
    return message

def is_date_inside(insider:Anime, outsider:Anime):
    return insider.date_start > outsider.date_start and insider.date_end < outsider.date_end


if __name__ == "__main__":
    url = "Dragon Ball Z "
    relateds = Relateds()
    relateds.set_first(url)
    relateds.next_step()
    relateds.set_displayed()
    print("\n\n")
    #animes = [Anime("Dragon Ball"), Anime("Dragon Ball Movie 1")]
    print(order_relateds(relateds.displayed))