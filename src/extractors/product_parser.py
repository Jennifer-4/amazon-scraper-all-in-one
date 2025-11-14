thonimport requests
from bs4 import BeautifulSoup
from datetime import datetime
from .utils_format import clean_text

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def parse_asin(asin: str) -> dict:
    url = f"https://www.amazon.com/dp/{asin}"
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    title = clean_text(soup.select_one("#productTitle").text if soup.select_one("#productTitle") else "")
    price_el = soup.select_one(".a-price .a-offscreen")
    price = float(price_el.text.replace("$", "").replace(",", "")) if price_el else None

    image_el = soup.select_one("#imgTagWrapperId img")
    image = image_el["src"] if image_el else None

    rating_el = soup.select_one("span[data-hook=rating-out-of-text]")
    rating = float(rating_el.text.split()[0]) if rating_el else None

    reviews_el = soup.select_one("#acrCustomerReviewText")
    review_count = int(reviews_el.text.split()[0].replace(",", "")) if reviews_el else None

    return {
        "title": title,
        "asin": asin,
        "category": None,
        "image": image,
        "sellerName": None,
        "sellerLink": None,
        "price": price,
        "currency": "USD",
        "rating": rating,
        "reviewCount": review_count,
        "variations": [],
        "variationCount": 0,
        "starBreakdown": {},
        "productVideos": [],
        "influencerVideos": [],
        "productLink": url,
        "lastUpdate": datetime.utcnow().isoformat() + "Z"
    }