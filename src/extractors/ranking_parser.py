thonimport requests
from bs4 import BeautifulSoup
from datetime import datetime
from .utils_format import clean_text

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_ranking(category: str) -> list:
    url = f"https://www.amazon.com/Best-Sellers-{category}/zgbs"
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("div.zg-grid-general-faceout")

    parsed = []
    for item in items:
        title_el = item.select_one("div.p13n-sc-truncate")
        link_el = item.select_one("a.a-link-normal")

        title = clean_text(title_el.text if title_el else "")
        asin = link_el["href"].split("/dp/")[1].split("/")[0] if link_el and "/dp/" in link_el["href"] else None

        parsed.append({
            "title": title,
            "asin": asin,
            "category": category,
            "image": None,
            "sellerName": None,
            "sellerLink": None,
            "price": None,
            "currency": "USD",
            "rating": None,
            "reviewCount": None,
            "variations": [],
            "variationCount": 0,
            "starBreakdown": {},
            "productVideos": [],
            "influencerVideos": [],
            "productLink": f"https://www.amazon.com/dp/{asin}" if asin else None,
            "lastUpdate": datetime.utcnow().isoformat() + "Z"
        })

    return parsed