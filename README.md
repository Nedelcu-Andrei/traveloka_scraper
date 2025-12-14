# Traveloka Scraper

A Python scraper that extracts hotel room and pricing data from Traveloka using **Playwright** and **XPath-based HTML parsing**.

The project handles dynamic content, bot protection (captcha), and non-trivial DOM structures.

---

## ✨ Features

- Uses **Playwright (Chromium)** for reliable rendering of dynamic content
- Supports **manual captcha solving** with persistent browser sessions
- Extracts:
  - Room names
  - Rate type
  - Shown currency
  - Prices (net / total / per stay / per night / original)
  - Taxes
  - Breakfast inclusion
  - Cancellation policy
  - Number of guests

---

## 📁 Project Structure

```text
root/
├── scraper/
│   ├── __init__.py
│   ├── sitemap_parser.py
│   ├── traveloka_scraper.py
│   └── traveloka_parser.py
├── logging_config.py
├── main.py
├── rates.json
├── .gitignore
└── README.md
```
---

## 🧠 Important Design Notes
- Captcha Handling
- Traveloka uses bot protection that may block automated requests.
- This scraper:
- Opens a non-headless browser
- Pauses execution if a captcha is detected
- Allows the user to solve the captcha manually
- Reuses the authenticated session locally (via Playwright persistent context)
- Session data is stored locally and ignored by Git.
- Room details and some prices are not nested together in the DOM.


## 🧩 Module Responsibilities

- **`traveloka_scraper.py`**  
  Handles browser automation, page loading, captcha detection, and session persistence using Playwright.

- **`traveloka_parser.py`**  
  Parses rendered HTML using XPath and extracts room and rate details.

- **`sitemap_parser.py`**  
  Parses sitemap data to discover hotel detail page URLs to scrape.

---

## 🛠 Requirements

- Python **3.9+**
- Playwright
- Chromium (installed via Playwright)

---

## 🚀 Setup & Installation

### 1 - Clone the repository

- bash
```
git clone https://github.com/Nedelcu-Andrei/traveloka_scraper
cd traveloka_scraper
```
- windows
```
.venv\Scripts\Activate.ps1
```
- macOS/Linux
```
source .venv/bin/activate
```
### 2 - Install dependencies
```
pip install -r requirements.txt
```
### 3 -  Install Playwright browsers
```
playwright install
```

### ▶️ Usage
- Run the scraper
```
python main.py
```
#### First Run Notes
- A browser window will open
- If a captcha appears, solve it manually
- Execution will resume automatically once the captcha is solved and prices are visible on the page

### 📄 Output
- Scraped data is saves as:
```
rates.json
```
- The file is generated in the root directory of the repository

### Easy Possible Future Improvements
- Fully automate hotel detail page URL discovery via sitemaps
- Schema validation (e.g., Pydantic)
- CLI arguments for input/output configuration
- Improved error handling and retry logic
