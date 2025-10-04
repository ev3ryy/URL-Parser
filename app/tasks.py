from sqlalchemy.orm import Session
from scraper import parse_site
from crud import create_item
from database import SessionLocal
from schemas import NewsItemCreate
from urllib.parse import urlparse

SITE_CONFIGS = {
    "lenta.ru": {
        "item": "a.card-mini._longgrid, a.card-big._longgrid",
        "title": "h3.card-mini__title, h3.card-big__title",
        "url": "::attr(href)",
        "snippet": "span.card-big__rightcol"
    }
}

async def run_scraping_task(*, urls: list[str], category: str):
    db: Session = SessionLocal()
    try:
        total_saved = 0

        for url in urls:
            domain = urlparse(url).netloc
            config = SITE_CONFIGS.get(domain)

            if not config:
                print(f"Нет конфигурации для {domain}")
                continue

            try:
                results = await parse_site(url, config, category)

                for data in results:
                    item_schema = NewsItemCreate(**data)
                    create_item(db, item_schema)

                print(f"Сохранено {len(results)} уникальных записей в бд")
                total_saved += len(results)
            except Exception as e:
                print(f"Ошибка в задаче парсинга: {e}")
    finally:
        db.close()