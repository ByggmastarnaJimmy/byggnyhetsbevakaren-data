import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

SOURCES = [
    {"name": "Byggfakta", "url": "https://www.byggfakta.se/nyheter", "category": "Projekt"},
    {"name": "Byggföretagen", "url": "https://www.byggforetagen.se/nyheter/", "category": "Bransch"},
    {"name": "Byggnads", "url": "https://www.byggnads.se/aktuellt/nyheter/", "category": "Arbetsmarknad"}
]

DUMMY_NEWS = {
    "Projekt": [{"titel": "Exempelprojekt i Stockholm", "källa": "Byggfakta", "url": "https://www.byggfakta.se/exempelprojekt"}],
    "Bransch": [{"titel": "Byggföretagen satsar på hållbarhet", "källa": "Byggföretagen", "url": "https://www.byggforetagen.se/hallbarhet"}],
    "Arbetsmarknad": [{"titel": "Byggnads lanserar nytt utbildningsprogram", "källa": "Byggnads", "url": "https://www.byggnads.se/utbildning"}]
}

def log(msg):
    print(f"[LOG] {msg}")

def fetch_news(url, max_items=5):
    log(f"Hämtar nyheter från {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        news_items = []
        for link in links:
            title = link.get_text(strip=True)
            href = link.get("href")
            if title and href and len(title) > 20:
                if not href.startswith("http"):
                    href = url.rstrip("/") + href
                news_items.append({"titel": title, "url": href})
            if len(news_items) >= max_items:
                break
        log(f"Hittade {len(news_items)} nyheter")
        return news_items
    except Exception as e:
        log(f"Fel vid hämtning från {url}: {e}")
        return []

def generate_summary(sources):
    log("Startar generering av sammanfattning")
    summary = {"datum": datetime.now().strftime("%Y-%m-%d"), "nyheter": {}, "dagens_pepp": "Byggbranschen växer – tillsammans bygger vi framtiden!"}
    for source in sources:
        news_list = fetch_news(source["url"])
        summary["nyheter"].setdefault(source["category"], [])
        if news_list:
            log(f"Lägger till {len(news_list)} nyheter för kategori {source['category']}")
            for item in news_list:
                summary["nyheter"][source["category"]].append({"titel": item["titel"], "källa": source["name"], "url": item["url"]})
        else:
            log(f"Ingen nyhet hittades för {source['name']}, använder fallback")
            summary["nyheter"][source["category"]].extend(DUMMY_NEWS[source["category"]])
    return summary

summary_data = generate_summary(SOURCES)
log("Sparar sammanfattning.json")
with open("sammanfattning.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, ensure_ascii=False, indent=2)
log("Klart!")
