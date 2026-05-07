import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://bizdirenepal.com"
SEARCH_URL = "https://bizdirenepal.com/kathmandu?search="


def get_listing_urls(keyword="restaurant", max_pages=2):
    """Get business detail page URLs from search results"""
    urls = []

    for page in range(1, max_pages + 1):
        page_url = f"{SEARCH_URL}{keyword}&page={page}"
        print(f"  Fetching listing page {page}: {page_url}")

        try:
            response = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.select("div.item-card7-desc a")
            for card in cards:
                href = card.get("href", "")
                if href.startswith("https://bizdirenepal.com/"):
                    urls.append(href)

        except requests.exceptions.RequestException as e:
            print(f"  Failed to fetch page {page}: {e}")

    urls = list(set(urls))  # remove duplicates
    print(f"  Found {len(urls)} unique listings")
    return urls


def scrape_business(url):
    """Scrape a single business detail page"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # business name
        name_tag = soup.select_one("h1.page-title")
        business_name = name_tag.get_text(strip=True) if name_tag else ""

        # phone number
        phone_tag = soup.select_one("a[href^='tel:']")
        phone = phone_tag["href"].replace("tel:", "").strip() if phone_tag else ""

        if business_name and phone:
            return {
                "name": business_name,
                "phone": phone,
                "business_name": business_name
            }

    except requests.exceptions.RequestException as e:
        print(f"  Failed to scrape {url}: {e}")

    return None


def scrape_to_csv(keyword="restaurant", output_path="data/scraped_contacts.csv", max_pages=2):
    """Main function - scrape and save to CSV"""
    print(f"\n--- Scraper Started: keyword='{keyword}' ---")

    urls = get_listing_urls(keyword=keyword, max_pages=max_pages)

    contacts = []
    for url in urls:
        result = scrape_business(url)
        if result:
            contacts.append(result)
            print(f"  Scraped: {result['business_name']} | {result['phone']}")

    if contacts:
        df = pd.DataFrame(contacts)
        df.to_csv(output_path, index=False)
        print(f"\n  Saved {len(contacts)} contacts to {output_path}")
    else:
        print("\n  No contacts scraped")

    return output_path