✨ Features

Uses Playwright (Chromium) for reliable rendering of dynamic content

Supports manual captcha solving with persistent browser sessions

Extracts:

Room names

Rate type

Shown currency

Prices (net / total / per stay / per night)

Taxes

Breakfast inclusion

Cancellation policy

Number of guests

Handles separated DOM structures (room data and prices rendered in different parts of the page)

Outputs structured data as JSON

Clean, reviewer-safe repository (no sessions, logs, or IDE files committed)

🧠 Important Design Notes
Captcha Handling

Traveloka uses bot protection that may block automated requests.

This scraper:

Opens a non-headless browser

Pauses execution if a captcha is detected

Allows the user to solve the captcha manually

Reuses the authenticated session locally (via Playwright persistent context)

Session data is stored locally and ignored by Git.

DOM Structure Reality

Room details and some prices are not nested together in the DOM.

📦 Project Structure
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

Module responsibilities

traveloka_scraper.py
Handles browser automation, page loading, captcha detection, and session persistence using Playwright.

traveloka_parser.py
Parses rendered HTML using XPath and extracts rooms details data.

sitemap_parser.py
Parses sitemap data to discover hotel URLs to scrape.


🛠 Requirements

Python 3.9+

Playwright

Chromium (installed via Playwright)

🚀 Setup & Installation

1️⃣ Clone the repository
git clone https://github.com/Nedelcu-Andrei/traveloka_scraper
cd traveloka_scraper

2️⃣ Create and activate a virtual environment
python -m venv .venv


Windows:

.venv\Scripts\Activate.ps1


macOS / Linux:

source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install Playwright browsers
playwright install

▶️ Usage

Run the scraper:

python main.py

First run

A browser window will open

If a captcha appears, solve it manually

Resume execution when prompted/ Or it will resume automatically after you solved the captcha and the price appears on the page.

Output

Scraped data is saved as:

rates.json

📄 Output Example

rates.json on main root directory of the repository.

📌 Easy Possible Future Improvements

Full automation on the hotels detail page URL's gathering from sitemaps.

Schema validation (e.g., Pydantic)

CLI arguments for input/output

Improved error handling and retries

