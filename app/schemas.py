from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsItemBase(BaseModel):
    title: str
    url: str
    content_snippet: Optional[str] = None
    category: str

class NewsItemCreate(NewsItemBase):
    pass

class NewsItem(NewsItemBase):
    id: int
    parse_date: datetime

    class Config:
        from_attributes = True