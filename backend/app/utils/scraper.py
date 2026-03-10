import requests
from bs4 import BeautifulSoup
import re
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress the annoying security warnings since we are doing this intentionally
warnings.simplefilter('ignore', InsecureRequestWarning)

URLS_TO_SCRAPE = [
    "https://ogaranya.com/",
    "https://www.ogaranya.com/about",
    "https://www.ogaranya.com/contact-us",
    "https://www.ogaranya.com/documentation",
    "https://www.ogaranya.com/integration",
    "https://www.ogaranya.com/documentation/v1/getting-started/",
    "https://www.ogaranya.com/documentation/v1/overview",
    "https://www.ogaranya.com/documentation/v1/api-token",
    "https://www.ogaranya.com/documentation/v1/authentication",
    "https://www.ogaranya.com/documentation/v1/sub-merchant-creation",
    "https://www.ogaranya.com/documentation/v1/country-code",
    "https://www.ogaranya.com/documentation/v1/transactions",
    "https://www.ogaranya.com/documentation/v1/product",
    "https://www.ogaranya.com/documentation/wallet/",
    "https://www.ogaranya.com/documentation/user-wallet",
    "https://www.ogaranya.com/documentation/merchant-wallet",
    "https://www.ogaranya.com/documentation/virtual-account",
    "https://www.ogaranya.com/bank/",
    "https://www.ogaranya.com/bank-enquiry",
    "https://www.ogaranya.com/documentation/v1/simulation",
    "https://www.ogaranya.com/documentation/v1/api-health",
    "https://www.ogaranya.com/command-list",
    "https://www.ogaranya.com/documentation/v1/faqs",
]

OUTPUT_FILE = "data/ogaranya_knowledge_base.txt"


def scrape_and_clean(url):
    print(f"Scraping {url}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # NOTICE THIS CHANGE: We added verify=False
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')

    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.extract()

    text = soup.get_text(separator='\n')

    cleaned_text = re.sub(r'\n+', '\n', text)
    cleaned_text = cleaned_text.strip()

    return cleaned_text


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("=== OGARANYA KNOWLEDGE BASE ===\n\n")

        for url in URLS_TO_SCRAPE:
            page_text = scrape_and_clean(url)

            if page_text:
                file.write(f"\n\n--- Source: {url} ---\n\n")
                file.write(page_text)
                print(f"Successfully saved data from {url}")

    print(f"\nDone! All data has been saved to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()