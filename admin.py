from flask import Flask, request, render_template_string, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

CANAL_DIR = "canais"
os.makedirs(CANAL_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Admin LeoFlix</title>
    <style>
        body {
            background-color: #111;
            color: #fff;
            font-family: sans-serif;
            padding: 20px;
        }
        h1 {
            color: #f00;
            text-align: center;
        }
        form {
            background: #222;
            padding: 20px;
            border-radius: 10px;
            max-width: 500px;
            margin: auto;
        }
        label, select, input, button {
            display: block;
            margin: 10px 0;
            width: 100%;
        }
        button {
            background-color: #f00;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #c00;
        }
    </style>
</head>
<body>
    <h1>Admin LeoFlix 🎬</h1>
    <form method="POST" action="/adicionar">
        <label>Link do YouTube:</label>
        <input type="text" name="link" required>

        <label>Escolha uma pasta existente:</label>
        <select name="pasta_existente">
            <option value="">-- Nenhuma --</option>
            {% for pasta in pastas %}
            <option value="{{ pasta }}">{{ pasta }}</option>
            {% endfor %}
        </select>

        <label>Ou crie uma nova pasta:</label>
        <input type="text" name="nova_pasta">

        <button type="submit">Salvar Link</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    pastas = [f.replace(".txt", "") for f in os.listdir(CANAL_DIR) if f.endswith(".txt")]
    return render_template_string(HTML_TEMPLATE, pastas=sorted(pastas))

@app.route("/adicionar", methods=["POST"])
def adicionar():
    link = request.form.get("link")
    pasta = request.form.get("pasta_existente")
    nova_pasta = request.form.get("nova_pasta").strip()

    nome_arquivo = nova_pasta if nova_pasta else pasta
    if not nome_arquivo:
        return "Você precisa escolher ou criar uma pasta. <a href='/'>Voltar</a>"

    arquivo_txt = os.path.join(CANAL_DIR, nome_arquivo + ".txt")
    with open(arquivo_txt, "a", encoding="utf-8") as f:
        f.write(link + "\n")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
