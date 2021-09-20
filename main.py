from flask import Flask, render_template, request, redirect, send_file
from scrapper import scrap
from exporter import save_to_file

fake_db = {}

app = Flask("Jobs")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jobs")
def jobs():
    word = request.args.get("word")
    if word:
        word = word.lower().strip()
        if word in fake_db:
            jobs = fake_db.get(word)
        else:
            jobs = scrap(word)
            fake_db[word] = jobs
    else:
        redirect("/")
    return render_template("jobs.html", jobs=jobs, word=word, length=len(jobs))

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = fake_db.get(word)
        if not jobs:
            raise Exception()

        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")
app.run()