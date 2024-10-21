from flask import flash, Flask, redirect, render_template, request, url_for, get_flashed_messages
from page_analyzer import db, validator
import psycopg2
import os
from dotenv import load_dotenv
import requests

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
        return redirect(url_for("index", code=302))
    try:
        id = repo.save_to_urls(url)
    except psycopg2.errors.UniqueViolation:
        id = repo.find_id(url)
        flash('Страница уже существует', "alert alert-info")
        return redirect(url_for("show_site", id=id))
    
    flash("Страница успешно добавлена", "alert alert-success")
    return redirect(url_for("show_site", id=id))


@app.get("/urls/<int:id>")
def show_site(id):
    messages = get_flashed_messages(with_categories=True)
    site = repo.find_site(id)
    checks = repo.get_checks_by_id(id)
    return render_template(
        "site.html",
        messages=messages,
        site=site,
        checks=checks,
    )


@app.get("/urls")
def show_sites():
    sites = repo.get_sites_and_checks()
    return render_template(
        "sites.html",
        sites=sites,
    )


@app.post("/urls/<int:id>/checks")
def post_checks(id):
    site = repo.find_site(id)
    try:
        request = requests.get(site['name'])
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "alert alert-danger")
        return redirect(url_for("show_site", id=id))
    
    if not request.ok:
        flash("Произошла ошибка при проверке", "alert alert-danger")
        return redirect(url_for("show_site", id=id))

    repo.save_to_checks(id, request.status_code, 'header', 'title', 'desc')
    
    flash("Страница успешно проверена", "alert alert-success")
    return redirect(url_for("show_site", id=id))
