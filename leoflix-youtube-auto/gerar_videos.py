import json

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
            "titulo": f"Vídeo LeoFlix {video_id}",
            "link": embed_link
        })

    estrutura = [{"canal": "LeoFlix Kids", "videos": videos}]
    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    gerar_json()
    print("✅ videos.json gerado com sucesso.")
