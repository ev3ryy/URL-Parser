import uvicorn
import asyncio
from typing import List, Optional
from fastapi import FastAPI, Depends, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, database, crud, schemas
from tasks import run_scraping_task
from pydantic import BaseModel

database.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Parser")

templates = Jinja2Templates(directory="templates")

class ParserRequest(BaseModel):
    url: str
    category: str

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(database.get_db)):
    items = crud.get_items(db, limit=50)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "items": items, "categories": ["Новости", "Товары", "Вакансии"]}

    )

@app.post("/run-parser/")
async def run_parser(req: ParserRequest, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    background_tasks.add_task(run_scraping_task, urls=[req.url], category=req.category)
    return {"message": f"Задача парсинга для '{req.category}' запущена в фоновом режиме"}

@app.get("/export-excel/")
async def export_excel(db: Session = Depends(database.get_db), category: Optional[str] = None):
    items = crud.get_items(db, category=category, limit=10000)
    if not items:
        raise HTTPException(status_code=404, detail="Нет данных для экспорта")
    
    filename = "parsed_data.xlsx"
    crud.items_to_excel(items, filename)

    return FileResponse(
        path=filename,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/items/", response_model=List[schemas.NewsItem])
def list_items(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    items = crud.get_items(db, skip=skip, limit=limit, category=category)
    return items

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)