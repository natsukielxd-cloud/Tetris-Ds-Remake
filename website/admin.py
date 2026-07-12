import json, os, time, webbrowser
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "blog-posts.json")
POST_TYPES = {"post": "[Post]", "event": "[Evento]", "announce": "[Aviso]", "update": "[Update]"}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    generate_js(posts)

def generate_js(posts):
    js = "const POSTS = " + json.dumps(posts, ensure_ascii=False) + ";"
    for d in ["website", "root_site"]:
        p = os.path.join(os.path.dirname(__file__), d, "posts.js")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(js)

def new_post():
    print("\n--- NUEVO POST ---")
    print("Tipo:")
    for k, v in POST_TYPES.items():
        print(f"  {k}: {v}")
    ptype = input("Tipo: ").strip() or "post"
    title = input("Titulo: ").strip()
    if not title:
        print("Cancelado.")
        return
    print("Contenido (linea vacia = terminar):")
    lines = []
    while True:
        l = input()
        if not l:
            break
        lines.append(l)
    content = "\n".join(lines)
    if not content:
        print("Cancelado.")
        return
    posts = load()
    posts.append({
        "id": int(time.time()),
        "type": ptype,
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save(posts)
    print(f"OK Post guardado! ({len(posts)} total)")

def list_posts():
    posts = load()
    if not posts:
        print("No hay posts.")
        return
    print(f"\n--- POSTS ({len(posts)}) ---")
    for i, p in enumerate(posts):
        tipo = POST_TYPES.get(p["type"], "[?]")
        print(f"{i+1}. {tipo} {p['title']} [{p['date']}]")
        primera = p['content'][:80].replace("\n", " ")
        print(f"   {primera}...")

def delete_post():
    posts = load()
    if not posts:
        print("No hay posts.")
        return
    print("\n--- BORRAR POST ---")
    for i, p in enumerate(posts):
        print(f"  {i+1}. {p['title']} [{p['date']}]")
    try:
        idx = int(input("Numero a borrar (0=salir): ")) - 1
        if 0 <= idx < len(posts):
            removed = posts.pop(idx)
            save(posts)
            print(f"Borrado: {removed['title']}")
    except:
        pass

def open_admin():
    url = "https://natsukielxd-cloud.github.io/Tetris-Ds-Remake/website/admin.html"
    print(f"Abriendo panel admin...\n{url}")
    webbrowser.open(url)

def main():
    print("=" * 45)
    print("  Tetris DS Demake - Admin Panel")
    print("=" * 45)
    while True:
        print("\nComandos:")
        print("  new      - Nuevo post/evento/aviso")
        print("  list     - Listar posts")
        print("  del      - Borrar post")
        print("  web      - Abrir admin.html oculto")
        print("  quit     - Salir")
        cmd = input("> ").strip().lower()
        if cmd == "quit":
            break
        elif cmd == "new":
            new_post()
        elif cmd == "list":
            list_posts()
        elif cmd == "del":
            delete_post()
        elif cmd == "web":
            open_admin()
        else:
            print("Comando desconocido.")

if __name__ == "__main__":
    main()
