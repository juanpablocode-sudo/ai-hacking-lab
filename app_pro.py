from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT)")
    c.execute("DELETE FROM users")  # limpia para evitar duplicados
    c.execute("INSERT INTO users VALUES ('admin', '1234')")
    conn.commit()
    conn.close()

init_db()

HTML = """
<h2>🔐 Login PRO</h2>

<form method="POST">
  <input name="user" placeholder="usuario">
  <input name="pass" placeholder="password">
  <button type="submit">Login</button>
</form>

<p>{{msg}}</p>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # 💣 VULNERABLE
        query = f"SELECT * FROM users WHERE user = '{user}' AND pass = '{password}'"
        result = c.execute(query).fetchone()

        if result:
            msg = "🔥 ACCESO CONCEDIDO 🔥"
        else:
            msg = "Acceso denegado"

        conn.close()

    return render_template_string(HTML, msg=msg)

app.run(debug=True)
