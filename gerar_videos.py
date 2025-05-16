import json

def extrair_id(link):
    if "watch?v=" in link:
        return link.split("watch?v=")[1].split("&")[0]
    return ""

def gerar_json():
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [l.strip() for l in f if l.strip()]

    videos_por_canal = {}

    for link in links:
        video_id = extrair_id(link)
        embed_link = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

        titulo = f"Título do vídeo {video_id}"
        canal = "LeoFlix Kids"

        if canal not in videos_por_canal:
            videos_por_canal[canal] = []

        videos_por_canal[canal].append({
            "titulo": titulo,
            "link": embed_link,
            "thumbnail": thumbnail
        })

    estrutura = [
        {
            "canal": canal,
            "videos": videos
        } for canal, videos in videos_por_canal.items()
    ]

    with open("videos.json", "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=2, ensure_ascii=False)

    print("✅ videos.json gerado com thumbnails.")

if __name__ == "__main__":
    gerar_json()
