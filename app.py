from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)

# Configuration MYSQL via variables d'environnement (pratique avec docker-compose)
db_config = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'docker_bdd'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
}

@app.route("/")
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Récupère un utilisateur
    cursor.execute("SELECT name, email FROM users LIMIT 1")
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("index.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)