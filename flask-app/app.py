from flask import Flask, render_template
import mysql.connector
import os
import time

app = Flask(__name__)

# Configuration MYSQL via variables d'environnement (pratique avec docker-compose)
db_config = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'docker_bdd'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
}


def get_db_connection(retries: int = 10, delay: float = 1.0):
    """Attempt to connect to the database with retries (useful when DB is starting).

    Raises the last exception if connection cannot be established.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(**db_config)
            return conn
        except mysql.connector.Error as e:
            last_exc = e
            app.logger.debug(f"DB connect attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    # if we exit loop, raise the last exception
    raise last_exc

@app.route("/")
def index():
    # use helper that waits a bit for the DB to be ready
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupère un utilisateur
    cursor.execute("SELECT name, email FROM users LIMIT 1")
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("index.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)