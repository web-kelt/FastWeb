from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND

from src.config import settings
from src.database.base import get_db
from src.app import app, templates
from src.models import News


@app.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    news_list = db_session.query(News).all()
    news_list = news_list[::-1]
    return templates.TemplateResponse('src/index.html',
                                      {'request': request,
                                       'app_name': settings.app_name,
                                       'news_list': news_list}
                                      )


@app.post('/add')
def add(title: str = Form(...), description: str = Form(...), db_session: Session = Depends(get_db)):
    new_news = News(title=title, description=description)
    db_session.add(new_news)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/delete/{todo_id}')
def delete(todo_id: int, db_session: Session = Depends(get_db)):
    news = db_session.query(News).filter_by(id=todo_id).first()
    db_session.delete(news)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
