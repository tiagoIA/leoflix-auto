import json
import os
import subprocess
import re

def extrair_id(link):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link)
    return match.group(1) if match else None

def gerar_json():
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [l.strip() for l in f if l.strip()]

    videos = []
    for link in links:
        video_id = extrair_id(link)
        if not video_id:
            print(f"ID inválido: {link}")
            continue
        embed_link = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        videos.append({
            "titulo": f"Vídeo LeoFlix ({video_id})",
            "link": embed_link
        })

    estrutura = [{"canal": "LeoFlix Kids", "videos": videos}]
    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=2, ensure_ascii=False)

    print("✅ videos.json gerado com sucesso.")

def git_push():
    subprocess.run(["git", "add", "videos.json"])
    subprocess.run(["git", "commit", "-m", "Atualização automática do catálogo com embeds"])

    token = os.environ['GH_TOKEN']
    repo_url = f"https://{token}@github.com/tiagoIA/leoflix-auto.git"
    subprocess.run(["git", "push", repo_url])

if __name__ == "__main__":
    gerar_json()
    git_push()

