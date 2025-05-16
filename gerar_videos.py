import json
import os
import subprocess

def extrair_id(link):
    if "watch?v=" in link:
        return link.split("watch?v=")[1].split("&")[0]
    return ""

def gerar_json():
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [l.strip() for l in f if l.strip()]

    videos = []
    for link in links:
        video_id = extrair_id(link)
        embed_link = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        videos.append({
            "titulo": f"Vídeo LeoFlix ({video_id})",
            "link": embed_link
        })

    estrutura = [{"canal": "LeoFlix Kids", "videos": videos}]
    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=2, ensure_ascii=False)

def git_push():
    subprocess.run(["git", "config", "--global", "user.name", "LeoFlix Auto"])
    subprocess.run(["git", "config", "--global", "user.email", "leoflix@auto.com"])

    subprocess.run(["git", "add", "videos.json"])
    subprocess.run(["git", "commit", "-m", "Atualização automática do catálogo"])
    subprocess.run([
        "git", "push",
        f"https://{os.environ['GH_TOKEN']}@github.com/tiagoIA/leoflix-auto.git",
        "main"
    ])

if __name__ == "__main__":
    gerar_json()
    git_push()
    print("✅ Catálogo atualizado com sucesso.")

