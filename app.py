from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="",
        database="user_db"
    )

@app.route('/user/<int:user_id>')
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return render_template('user.html', user=user)
    else:
        return "<h1>User not found</h1>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
