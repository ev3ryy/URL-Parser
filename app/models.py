from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timezone

class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    content_snippet = Column(String)
    category = Column(String, index=True)
    parse_date = Column(DateTime, default=datetime.now(timezone.utc))