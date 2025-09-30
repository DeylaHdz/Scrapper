from flask import request, jsonify
from crawler import get_domain_links, save_links_to_file, extract_from_links_file
from extractors import extract_from_file, extract_from_url
from utils import limit_text, guess_headings
import requests
from pathlib import Path
import os
import slugify

def register_routes(app):
    @app.post("/extract")
    def extract():
        try:
            limit_param = request.form.get("limit") or request.args.get("limit")
            limit = int(limit_param) if limit_param else None

            output_dir = "documentos"
            os.makedirs(output_dir, exist_ok=True)

            # Subida de archivo
            if "file" in request.files and request.files["file"].filename:
                file = request.files["file"]
                filename = file.filename
                file_bytes = file.read()
                text, meta = extract_from_file(filename, file_bytes)

                # Nombre de salida
                base_name = Path(filename).stem
                safe_name = slugify.slugify(base_name)
                filepath = os.path.join(output_dir, f"{safe_name}.txt")

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)

                headings = guess_headings(text)
                return jsonify({
                    "ok": True,
                    "source": "upload",
                    "filename": filename,
                    "saved_as": filepath,
                    "metadata": meta | {"word_count": len(text.split())},
                    "headings": headings,
                    "text": limit_text(text, limit)
                })

            url = request.form.get("url") or request.args.get("url")
            if url:
                text, meta = extract_from_url(url)

                domain = urlparse(url).netloc.replace("www.", "")
                short_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:6]
                safe_name = slugify.slugify(domain) + "-" + short_hash
                filepath = os.path.join(output_dir, f"{safe_name}.txt")

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)

                headings = guess_headings(text)
                return jsonify({
                    "ok": True,
                    "source": "url",
                    "url": url,
                    "saved_as": filepath,
                    "metadata": meta | {"word_count": len(text.split())},
                    "headings": headings,
                    "text": limit_text(text, limit)
                })

            return jsonify({"ok": False, "error": "Proporciona un archivo o una URL."}), 400

        except requests.RequestException as e:
            return jsonify({"ok": False, "error": f"Error HTTP al descargar: {e}"}), 502
        except Exception as e:
            return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

    @app.post("/crawl")
    def crawl_domain():
        url = request.form.get("url")
        if not url:
            return jsonify({"ok": False, "error": "Falta parámetro url"}), 400
        try:
            links = get_domain_links(url)
            file = save_links_to_file(links, url)   # 👈 ahora incluye el dominio en el nombre
            return jsonify({"ok": True, "url": url, "link_count": len(links), "file": file})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500

    @app.post("/extract_links")
    def extract_links():
        try:
            # Si el archivo viene subido desde el formulario
            if "file" in request.files and request.files["file"].filename:
                file = request.files["file"]
                filepath = file.filename
                file.save(filepath)  # Guardamos el .txt
            else:
                filepath = request.form.get("file") or "enlaces.txt"

            extract_from_links_file(filepath)
            return jsonify({
                "ok": True,
                "file": filepath,
                "msg": f"Documentos guardados en carpeta 'documentos'"
            })
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 500