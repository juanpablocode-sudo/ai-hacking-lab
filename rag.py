from flask import Flask, request, render_template_string

app = Flask(__name__)

# 📄 "Documento interno" (esto simula base de datos / PDF)
DOCUMENTO = """
Manual interno de la empresa:

- Usuario: admin
- PASSWORD_ADMIN=supersecreto123

No compartir esta información.
"""

def rag_ai(user_input):
    user = user_input.lower()

    # Simulación de IA con contexto
    contexto = DOCUMENTO

    # 🔒 comportamiento "seguro"
    if "password" in user or "contraseña" in user:
        return "No puedo revelar contraseñas."

    # 💣 VULNERABILIDADES

    # 1. Prompt injection
    if "ignora" in user:
        return contexto

    # 2. Debug leak
    if "debug" in user:
        return f"[DEBUG]\n{contexto}"

    # 3. Extracción indirecta
    if "resumen completo" in user:
        return f"Resumen:\n{contexto}"

    return "Puedo ayudarte con información general de la empresa."

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG AI</title>
</head>
<body>
    <h2>📄 Chat con memoria (RAG)</h2>
    <form method="POST">
        <input name="msg" placeholder="Preguntá algo..." />
        <button type="submit">Enviar</button>
    </form>
    <p><b>Respuesta:</b> {{response}}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form["msg"]
        response = rag_ai(user_input)
    return render_template_string(HTML, response=response)

app.run(host="0.0.0.0", port=10000)
