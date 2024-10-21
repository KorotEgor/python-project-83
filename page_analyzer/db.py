import psycopg2
from psycopg2.extras import RealDictCursor


class SiteRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def save_to_urls(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                    (url,),
                )
                id = cur.fetchone()[0]

        return id
    
    def save_to_checks(self, url_id, status_code, h1, title, description):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO url_checks (url_id, status_code, h1, title, description) VALUES (%s, %s, %s, %s, %s);",
                    (url_id, status_code, h1, title, description),
                )

    def get_sites(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls;")
                return cur.fetchall()

    def get_checks_by_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """SELECT * 
                    FROM url_checks 
                    WHERE url_id = %s 
                    ORDER BY created_at DESC
                    ;""",
                    (url_id,),
                )
                return cur.fetchall()
    
    def get_sites_and_checks(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """WITH last_check AS (
                        SELECT url_id, MAX(id) AS id
                        FROM url_checks
                        GROUP BY url_id
                    )
                    SELECT
                        urls.id AS id, 
                        urls.name AS name, 
                        url_checks.created_at AS created_at, 
                        url_checks.status_code AS status_code 
                    FROM urls
                    LEFT JOIN last_check
                    ON last_check.url_id = urls.id 
                    LEFT JOIN url_checks
                    ON last_check.id = url_checks.id
                    ORDER BY urls.id DESC
                    ;""",
                )
                return cur.fetchall()

    def find_id(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s;", (url,))
                id = cur.fetchone()["id"]

        return id

    def find_site(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s;", (id,))
                return cur.fetchone()
