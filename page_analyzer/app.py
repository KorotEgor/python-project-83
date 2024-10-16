from email import message
from flask import flash, Flask, redirect, render_template, request, url_for, get_flashed_messages
from page_analyzer import db, validator
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

repo = db.SiteRepository(app.config["DATABASE_URL"])


@app.route("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "index.html",
        messages=messages,
    )


@app.post("/urls")
def post_sites():
    url = request.form.to_dict()["url"]
    url, error = validator.validate(url)
    
    if error:
        flash(error, "alert alert-danger")
        return redirect(url_for('index'))

    id = repo.save(url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_site"), code=302)


@app.get("/urls/<id>")
def show_site(id):
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "index.html",
        messages=messages,
    )
