import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)

async def fetch_page(url: str) -> str:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP ошибка при получении {url}: {e}")
        return ""
    except httpx.RequestError as e:
        logging.error(f"Ошибка запроса к {url}: {e}")
        return ""
    
def extract_text(el, selector: str, base_url: str = "") -> Optional[str]:
    if "::attr(" in selector:
        css, attr = selector.split("::attr(")
        attr = attr.replace(")", "")
        tag = el.select_one(css.strip()) if css.strip() else el
        if tag and tag.has_attr(attr):
            value = tag.get(attr).strip()
            return urljoin(base_url, value) if attr == "href" else value
        return None
    else:
        tag = el.select_one(selector) if selector else el
        return tag.get_text(strip=True) if tag else None

async def parse_site(url: str, config: dict, category: str) -> list[dict]:
    html = await fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for item in soup.select(config["item"]):
        try:
            title = extract_text(item, config["title"]) if config.get("title") else item.get_text(strip=True)
            item_url = extract_text(item, config.get("url", ""), base_url=url)
            snippet = extract_text(item, config.get("snippet", "")) or "—"

            if title and item_url:
                results.append({
                    "title": title,
                    "url": item_url,
                    "content_snippet": snippet,
                    "category": category
                })
        except Exception as e:
            logging.warning(f"Ошибка при обработке элемента: {e}")
            continue

    logging.info(f"Найдено {len(results)} элементов для {url}")
    return results
