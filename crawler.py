from urllib.parse import urljoin, urlparse
import os
import slugify
from extractors import extract_from_url
import hashlib


# Playwright
from playwright.sync_api import sync_playwright

USER_AGENT = "SimpleDocScraper/1.0 (+for demo; contact admin@example.com)"

def get_domain_links(start_url: str) -> list[str]:
    """
    Obtiene todos los enlaces de un dominio usando Playwright (renderizado con JS).
    """
    links = set()
    domain = urlparse(start_url).netloc.replace("www.", "")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(start_url, timeout=60000)
        page.wait_for_load_state("networkidle")

        anchors = page.query_selector_all("a[href]")
        for a in anchors:
            href = a.get_attribute("href")
            if not href:
                continue
            full_url = urljoin(start_url, href)
            netloc = urlparse(full_url).netloc.replace("www.", "")
            if domain in netloc:  # incluye subdominios
                links.add(full_url.split("#")[0])

        browser.close()

    return sorted(links)


def save_links_to_file(links: list[str], base_url: str, output_dir="") -> str:
    """
    Guarda los enlaces en un archivo llamado <dominio>-enlaces.txt
    """
    domain = urlparse(base_url).netloc.replace("www.", "")
    safe_domain = slugify.slugify(domain)
    filename = f"{safe_domain}-enlaces.txt"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
    else:
        filepath = filename

    with open(filepath, "w", encoding="utf-8") as f:
        for l in links:
            f.write(l + "\n")
    return filepath


def extract_from_links_file(file="enlaces.txt", output_dir="documentos"):
    os.makedirs(output_dir, exist_ok=True)
    with open(file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        try:
            text, meta = extract_from_url(url)

            # Base del nombre: title o path de la URL
            title = meta.get("title") or urlparse(url).path.strip("/").replace("/", "_") or "documento"

            # Hash corto de la URL para que no se repita
            short_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:6]

            safe_title = slugify.slugify(title) or "documento"
            filename = f"{safe_title}-{short_hash}.txt"

            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as out:
                out.write(text)

            print(f"Guardado {filepath}")
        except Exception as e:
            print(f"Error con {url}: {e}")