from dbm import error
from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from site_repository import SiteRepository
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        'index.html',
    )


@app.route("/")
def post_sites():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            ''
        )
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for(''), code=302)


def find(id):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        return cur.fetchone()


def save(site_data):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id",
            (site_data['name'],)
        )
        site_data['id'] = cur.fetchone()[0]
    conn.commit()
    return site_data['id']


@app.get('urls/<id>')
def show_site(id):



def validate(course_dict):
    errs = {}
    if not course_dict.get('paid'):
        errs['paid'] = "Can't be blank"
    if not course_dict.get('title'):
        errs['title'] = "Can't be blank"
    return errs