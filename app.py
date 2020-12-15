import json

from flask import Flask, render_template, request, redirect, url_for
from Anime import *
from Relateds import *

app = Flask(__name__)

to_remove = []
relateds_obj = Relateds()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/relateds", methods=['GET', 'POST'])
def relateds():
    global relateds_obj
    relateds_obj = Relateds()
    clear_remove()
    if request.method == "POST":
        anime = request.form["firstAnime"]
        if anime:
            return redirect(url_for("relateds_step", anime=anime))
        return render_template("relateds.html")

    return render_template("relateds.html")


@app.route("/relateds/<anime>", methods=["GET", "POST"])
def relateds_step(anime):
    global to_remove
    if request.method == "POST":
        for anime in to_remove:
            relateds_obj.removed_append(anime)


        if "sort" in request.form:
            sort_option = request.form.get('sort_select')
            return redirect(url_for("sorteds", sort_option=sort_option))

        if "nextStep" in request.form:
            relateds_obj.next_step()

        return render_template("relateds_step.html", olds=relateds_obj.old, news=relateds_obj.new)
    clear_remove()
    if relateds_obj.first_anime is None:  # If refresh page doesn't add the anime again
        relateds_obj.set_first(anime)
    return render_template("relateds_step.html", olds=relateds_obj.old, news=relateds_obj.new)

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

@app.route("/sorteds", methods=["GET", "POST"])
def sorteds():
    sort_option = request.args.get('sort_option', None)
    relateds_obj.set_sorted()
    relateds_obj.sort_sorted(sort_option)
    return render_template("sorteds.html", sorteds=relateds_obj.sorted, sort_option=sort_option)

@app.route("/sort_reverse", methods=["POST"])
def sort_reverse():
    if (request.method == "POST"):
        jsonResponse = json.loads(request.data.decode('utf-8'))
        sort_option = jsonResponse["sort_option"]
        relateds_obj.sort_reverse()
        relateds_obj.sort_sorted(sort_option)
        print("Reversed")
        return render_template("sorteds.html", sorteds=relateds_obj.sorted, sort_option=sort_option), 200

def clear_remove():
    global to_remove
    to_remove = []

app.run()
app.config["TEMPLATES_AUTO_RELOAD"] = True
