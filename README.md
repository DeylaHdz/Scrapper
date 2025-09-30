# Scrapper

This project is a **Flask web scraper** for documents and websites (PDF, DOCX, TXT, HTML — including React/Vite SPAs via Playwright).
It allows you to upload files, scrape a single URL, crawl a domain for all internal links, and extract the content into `.txt` files.

---

## 🚀 Getting Started

### 📋 Prerequisites

* Python **3.8+**
* `pip` package manager
* Chromium browser for Playwright

### 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DeylaHdz/Scrapper.git
   cd Scrapper
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Install Chromium for Playwright:

   ```bash
   playwright install chromium
   ```

---

## ▶️ Usage

Run the Flask server:

```bash
flask run
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Available features:

* **Upload File** → Upload `.pdf`, `.docx`, or `.txt` and extract text (saved as `.txt` in `documentos/`).
* **Extract from URL** → Provide a URL and extract the rendered page text (SPA supported with Playwright). Output saved in `documentos/`.
* **Crawl Domain** → Provide a base URL, collect all internal links into `<domain>-enlaces.txt`.
* **Extract from Links File** → Upload the `.txt` file of links and extract each page/document into `documentos/`.

All outputs are stored in the `documentos/` folder as `.txt`.

---

## ⚙️ Configuration

* **`requirements.txt`** includes all dependencies (`Flask`, `pdfplumber`, `playwright`, etc.).
* **Playwright** is used to render React/Vite/SPA sites before text extraction.
* File names are generated safely with `python-slugify`, with unique hashes to avoid overwriting.

---

## 📌 Notes

* For crawling SPAs (e.g., React, Vue, Next.js, Vite), Playwright ensures that JavaScript-rendered content is captured.
* By default, extracted text is **cleaned and normalized** before saving.
* Each extraction returns a JSON response via the API and also saves the `.txt` file in `documentos/`.

