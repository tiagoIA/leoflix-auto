
from flask import Flask, request, render_template_string, redirect
import os
from datetime import datetime
import subprocess
import json

app = Flask(__name__)

LINKS_DIR = "links"
VIDEO_JSON = "videos.json"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>LeoFlix Admin</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background-color: #f2f2f2; }
        h1 { color: #d10a1b; }
        form { background: white; padding: 20px; border-radius: 8px; max-width: 500px; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input[type="text"], select { width: 100%; padding: 8px; margin-top: 5px; }
        .submit { margin-top: 20px; background-color: #d10a1b; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .submit:hover { background-color: #b00918; }
    </style>
</head>
<body>
    <h1>🎬 LeoFlix Admin</h1>
    <form method="POST">
        <label for="link">📎 Link do vídeo</label>
        <input type="text" name="link" required>

        <label for="folder">📁 Escolher pasta existente</label>
        <select name="folder">
            <option value="">-- Criar nova pasta --</option>
            {% for pasta in pastas %}
                <option value="{{ pasta }}">{{ pasta }}</option>
            {% endfor %}
        </select>

        <label for="new_folder">📂 Nome da nova pasta (se for criar)</label>
        <input type="text" name="new_folder">

        <button type="submit" class="submit">Adicionar Link</button>
    </form>
</body>
</html>
"""

def salvar_link_em_pasta(link, pasta):
    os.makedirs(LINKS_DIR, exist_ok=True)
    caminho = os.path.join(LINKS_DIR, pasta + ".txt")
    with open(caminho, "a") as f:
        f.write(link.strip() + "\n")

def gerar_videos_json():
    estrutura = []
    for arquivo in os.listdir(LINKS_DIR):
        if not arquivo.endswith(".txt"): continue
        nome = arquivo.replace("_", " ").replace(".txt", "").title()
        with open(os.path.join(LINKS_DIR, arquivo), "r") as f:
            links = [l.strip() for l in f if l.strip()]
        videos = []
        for link in links:
            if "watch?v=" in link:
                video_id = link.split("watch?v=")[1].split("&")[0]
                embed = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
                videos.append({"titulo": f"Vídeo LeoFlix ({video_id})", "link": embed})
        estrutura.append({"canal": nome, "videos": videos})
    with open(VIDEO_JSON, "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=2, ensure_ascii=False)

def git_push():
    subprocess.run(["git", "add", "videos.json", LINKS_DIR], check=True)
    subprocess.run(["git", "commit", "-m", f"Atualizado via admin web: {datetime.now()}"], check=True)
    subprocess.run(["git", "push"], check=True)

@app.route("/", methods=["GET", "POST"])
def index():
    os.makedirs(LINKS_DIR, exist_ok=True)
    pastas = [f.replace(".txt", "") for f in os.listdir(LINKS_DIR) if f.endswith(".txt")]
    if request.method == "POST":
        link = request.form.get("link")
        folder = request.form.get("folder")
        new_folder = request.form.get("new_folder").strip().lower().replace(" ", "_")

        nome_final = new_folder if new_folder else folder
        if not nome_final:
            return "Erro: escolha uma pasta ou crie uma nova.", 400

        salvar_link_em_pasta(link, nome_final)
        gerar_videos_json()
        try:
            git_push()
        except Exception as e:
            return f"Erro ao fazer push: {e}", 500

        return redirect("/")

    return render_template_string(HTML_TEMPLATE, pastas=pastas)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
