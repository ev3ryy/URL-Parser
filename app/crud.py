from sqlalchemy.orm import Session
import models, schemas
from typing import List, Optional
import pandas as pd

def get_items(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[models.NewsItem]:
    query = db.query(models.NewsItem)
    if category:
        query = query.filter(models.NewsItem.category == category)
    return query.offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.NewsItemCreate):
    if db.query(models.NewsItem).filter(models.NewsItem.url == item.url).first():
        return None
    
    db_item = models.NewsItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def items_to_excel(items: List[models.NewsItem], filename: str = "parsed_data.xlsx"):
    data = [{
        'ID': item.id,
        'Заголовок': item.title,
        'URL': item.url,
        'Содержание': item.content_snippet,
        'Категория': item.category,
        'Дата парсинга': item.parse_date.strftime('%Y-%m-%d %H:%M:%S')
    } for item in items]

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename