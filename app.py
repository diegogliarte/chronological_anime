import json

from flask import Flask, render_template, request, redirect, url_for, session
from Relateds import *

app = Flask(__name__)
to_remove = []  # TODO Change to Relateds param
relateds = Relateds()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/relateds", methods=['GET', 'POST'])
def relateds():
    global relateds
    relateds = Relateds()
    clear_remove()

    if request.method == "POST" and (anime := request.form["firstAnime"]):
        if relateds.first_anime is None:  # If refresh page doesn't add the anime again
            relateds.set_first(anime)
        return redirect(url_for("relateds_step"))

    return render_template("relateds.html")


@app.route("/relateds/step", methods=["GET", "POST"])
def relateds_step():
    if request.method == "POST":
        to_remove_append()
        submit = (request.form["submitter"])

        if submit == "table":
            return redirect(url_for("table"))

        if submit == "timeline":
            return redirect(url_for("timeline"))

        if submit == "nextStep":
            relateds.next_step()
            clear_remove()

        return redirect(url_for("relateds_step"))

    return render_template("relateds_step.html", olds=relateds.old, news=relateds.new, to_remove=to_remove)


@app.route("/delete", methods=["POST"])
def delete():
    if (request.method == "POST"):
        jsonResponse = json.loads(request.data.decode('utf-8'))
        id = jsonResponse["id"]

        if id in to_remove:
            to_remove.remove(id)  # TODO When you add to remove and press sort, the animes are not crossed anymore
        else:
            to_remove.append(id)

        return render_template("relateds.html")


@app.route("/table", methods=['GET', 'POST'])
def table():
    relateds.set_displayed()
    return render_template("table.html", animes=relateds.displayed)


def clear_remove():
    global to_remove
    to_remove = []


def to_remove_append():
    for anime in to_remove:
        relateds.removed_append(anime)


def to_remove_remove():
    for anime in to_remove:
        relateds.removed_remove(anime)


app.run(debug=True)
