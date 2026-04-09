from flask import Flask, request, render_template_string, redirect
import sqlite3

app = Flask(__name__)

# DB INIT
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS chats (user TEXT, message TEXT, response TEXT)")

    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES ('admin', '1234')")

    conn.commit()
    conn.close()

init_db()

SECRET = "API_KEY_SUPER_SECRETA"

# UI CHATGPT STYLE
HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    font-family: Arial;
    display: flex;
    background: #343541;
    color: white;
}

.sidebar {
    width: 200px;
    background: #202123;
    padding: 10px;
}

.chat {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
}

.input-box {
    display: flex;
    padding: 10px;
    background: #40414f;
}

input {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 5px;
}

button {
    margin-left: 10px;
    padding: 10px;
    background: #19c37d;
    border: none;
    border-radius: 5px;
    color: white;
}

.msg-user {
    text-align: right;
    margin: 10px;
}

.msg-bot {
    text-align: left;
    margin: 10px;
    color: #19c37d;
}
</style>
</head>

<body>

<div class="sidebar">
<h3>Chats</h3>
</div>

<div class="chat">
<div class="messages">
{{messages}}
</div>

<form method="POST" class="input-box">
<input name="msg" placeholder="Enviar mensaje...">
<button>Enviar</button>
</form>
</div>

</body>
</html>
"""

def fake_ai(msg):
    if "debug" in msg:
        return SECRET
    return "Respuesta IA"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]

        conn = sqlite3.connect("chat.db")
        c = conn.cursor()

        # 💣 SQL INJECTION
        query = f"SELECT * FROM users WHERE user = '{user}' AND pass = '{password}'"
        result = c.execute(query).fetchone()

        conn.close()

        if result:
            return redirect(f"/chat?user={user}")

    return """
    <h2>Login</h2>
    <form method="POST">
        <input name="user">
        <input name="pass">
        <button>Login</button>
    </form>
    """

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user = request.args.get("user")

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()

    if request.method == "POST":
        msg = request.form["msg"]
        response = fake_ai(msg)

        c.execute("INSERT INTO chats VALUES (?, ?, ?)", (user, msg, response))
        conn.commit()

    chats = c.execute("SELECT message, response FROM chats WHERE user=?", (user,)).fetchall()

    conn.close()

    messages_html = ""
    for m, r in chats:
        messages_html += f"<div class='msg-user'>{m}</div>"
        messages_html += f"<div class='msg-bot'>{r}</div>"

    return render_template_string(HTML, messages=messages_html)

app.run(host="0.0.0.0", port=10000)
