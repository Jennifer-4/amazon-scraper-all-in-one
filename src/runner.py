thonimport json
import logging
from pathlib import Path
from extractors.product_parser import parse_asin
from extractors.ranking_parser import parse_ranking
from outputs.exporters import export_json
from configparser import ConfigParser

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_settings():
    cfg_path = Path(__file__).parent / "config" / "settings.example.json"
    with open(cfg_path, "r") as f:
        return json.load(f)

def load_asins():
    asin_file = Path(__file__).parents[1] / "data" / "asin_list.sample.txt"
    if not asin_file.exists():
        return []
    with open(asin_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    settings = load_settings()
    asins = load_asins()

    results = []

    for asin in asins:
        try:
            logging.info(f"Scraping ASIN: {asin}")
            product = parse_asin(asin)
            results.append(product)
        except Exception as e:
            logging.error(f"Error parsing ASIN {asin}: {e}")

    # Example of ranking scrape
    if settings.get("scrape_rankings", False):
        for category in settings.get("ranking_categories", []):
            try:
                logging.info(f"Scraping ranking: {category}")
                ranking_items = parse_ranking(category)
                results.extend(ranking_items)
            except Exception as e:
                logging.error(f"Error parsing ranking {category}: {e}")

    output_path = Path(__file__).parents[1] / "data" / "sample_output.json"
    export_json(results, output_path)
    logging.info(f"Saved output → {output_path}")

if __name__ == "__main__":
    main()