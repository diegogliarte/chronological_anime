from flask import Flask, render_template, request, redirect, url_for, session
from Relateds import *
from utils import *

app = Flask(__name__)
relateds = Relateds()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/relateds", methods=['GET', 'POST'])
def relateds():
    global relateds
    relateds = Relateds()

    if request.method == "POST" and (anime := request.form["firstAnime"]):
        if relateds.first_anime is None:  # If refresh page doesn't add the anime again
            relateds.set_first(anime)
        return redirect(url_for("relateds_step"))

    return render_template("relateds.html")


@app.route("/relateds/step", methods=["GET", "POST"])
def relateds_step():
    if request.method == "POST":
        submit = (request.form["submitter"])

        if submit == "table":
            return redirect(url_for("table"))

        if submit == "order":
            return redirect(url_for("order"))

        if submit == "nextStep":
            relateds.next_step()

    return render_template("steps.html", olds=relateds.old, news=relateds.new,
                           removeds=relateds.pending_removed)


@app.route("/delete", methods=["POST"])
def delete():
    if (request.method == "POST"):
        jsonResponse = json.loads(request.data.decode('utf-8'))
        url = jsonResponse["url"]
        relateds.toggle_pending_remove(url)
        return render_template("relateds.html")


@app.route("/table", methods=['GET', 'POST'])
def table():
    relateds.set_displayed()
    if (len(relateds.displayed) == 0):
        score = 0
        episodes = 0
        duration = 0
    else:
        score = round(sum(anime.score for anime in relateds.displayed) / len(relateds.displayed), 3)
        episodes = sum(anime.episodes for anime in relateds.displayed)
        duration = sum([anime.total_duration for anime in relateds.displayed], datetime.timedelta())
    return render_template("table.html", animes=relateds.displayed, score=score, episodes=episodes, duration=duration)


@app.route("/order", methods=['GET', 'POST'])
def order():
    relateds.set_displayed()
    message = order_relateds(relateds.displayed)
    return render_template("order.html", message=message.split("\n"))


app.run(debug=True)
