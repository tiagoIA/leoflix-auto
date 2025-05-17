from flask import Flask, request, render_template_string, redirect
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pasta = request.form.get("pasta")
        link = request.form.get("link")

        if not pasta or not link:
            return "Preencha todos os campos", 400

        os.makedirs("pastas", exist_ok=True)
        caminho = os.path.join("pastas", f"{pasta}.txt")
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(link.strip() + "\n")

        return redirect("/")

    return render_template_string("""
        <h2>Adicionar novo link</h2>
        <form method="post">
            Pasta: <input type="text" name="pasta"><br>
            Link: <input type="text" name="link"><br>
            <button type="submit">Salvar</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(debug=True)