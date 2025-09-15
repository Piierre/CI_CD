from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuration MYSQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'docker_bdd',
    'port' : 3306
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