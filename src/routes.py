import httpx
import json
from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND

from src.config import settings
from src.database.base import get_db
from src.app import app, templates
from src.models import News, User

github_client_id = '0cff75a071cb22116051'
github_client_secret = '0ee1ae9a3470e37c63fd5b95e0448fe6ee24e897'
git = 'https://github.com/login/oauth/authorize?client_id'


#---------------------------------------------------------------#
#____________________//Before registration//____________________#
#_______________________________________________________________#


@app.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    news_list = db_session.query(News).all()
    news_list = news_list[::-1]

    dost_news_list = [] #список новостей по жанру достижения кафедры
    sport_news_list = [] #список новостей по жанру спорт
    stud_news_list = [] #список новостей по жанру студентам
    nau_news_list = [] #список новостей по жанру наука

    for news in news_list:
        if news.genre == "dost":
                dost_news_list.append(news)
                continue
        if news.genre == "sport":
                dost_news_list.append(news)
                continue
        if news.genre == "stud":
                dost_news_list.append(news)
                continue
        if news.genre == "nau":
                dost_news_list.append(news)
                continue

    user = None
    return templates.TemplateResponse('src/index.html',
                                      {'request': request,
                                       'app_name': settings.app_name,
                                       'news_list': news_list,
                                       'user': user,
                                       'dost': dost_news_list,
                                       'sport': sport_news_list,
                                       'stud': stud_news_list,
                                       'nau': nau_news_list
                                       })


@app.post('/add')
def add(    title: str = Form(...),
            description: str = Form(...),
            genre: str = Form(default = "other"),
            db_session: Session = Depends(get_db)
        ):
        print(f"\n\n\n[INFO] title = {title}\n[INFO] description = {description}\n[INFO] genre = {genre}\n\n\n")
        if genre == None:
                genre = ""
        new_news = News(title=title, description=description, genre=genre)
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


#---------------------------------------------------------------#
#_________________//Registration with GitHub//__________________#
#_______________________________________________________________#

# переход на git для прохождения авторизации
@app.get('/github-login')
async def github_login():
        return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get('/github-psevdo-login')
async def github_psevdo_login(request: Request, db_session: Session = Depends(get_db)):
        user = User('anetto', 'xx34324', True)
        news_list = db_session.query(News).all()
        news_list = news_list[::-1]
        return templates.TemplateResponse('src/index.html',
                                        {'request': request,
                                        'app_name': settings.app_name,
                                        'news_list': news_list,
                                        'user': user}
                                        )


# получение информации и САМОЕ ГЛАВНОЕ - access token
@app.get('/github-code')
async def github_code(code: str, request: Request, db_session: Session = Depends(get_db)):
        params = {
                'client_id': github_client_id,
                'client_secret': github_client_secret,
                'code': code
        }
        headers = {'Accept': 'application/json'}
        async with httpx.AsyncClient() as client:
                response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
        response_json = response.json()
        access_token = response_json['access_token']
        print(access_token)
        async with httpx.AsyncClient() as client:
                headers.update({'Authorization': f'Bearer {access_token}'})
                response = await client.get('https://api.github.com/user', headers=headers)
        data = response.json()
        #return data
        #url = app.url_path_for('home')
        #return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
        news_list = db_session.query(News).all()
        news_list = news_list[::-1]
        user = User('anetto', 'xx34324', True)
        return templates.TemplateResponse('src/index.html',
                                        {'request': request,
                                        'app_name': settings.app_name,
                                        'news_list': news_list,
                                        'user': user}
                                        )

# проверка получения информации о пользователе используя только access token
#@app.get('/info')
#async def github_code():
#        headers = {'Accept': 'application/json'}
#        access_token = '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'
#        async with httpx.AsyncClient() as client:
#                headers.update({'Authorization': f'Bearer {access_token}'})
#                response = await client.get('https://api.github.com/user', headers=headers)
#        data = response.json()
#        print(access_token)
#        return data


#---------------------------------------------------------------#
#____________________//After registraion//______________________#
#_______________________________________________________________#


#---------------------------------------------------------------#
#__________________________//Search//___________________________#
#_______________________________________________________________#

@app.get('/search')
def search(   request: Request,
              val: str = "",
              db_session: Session = Depends(get_db)
        ):
        news_list = db_session.query(News).all()
        finally_news_set = []
        for i in news_list:
                if val in i.title:
                        finally_news_set.append(i)
                        continue
                if val in i.description:
                        finally_news_set.append(i)
                        continue
        finally_news_set = finally_news_set[::-1]
        user = None
        return templates.TemplateResponse('src/index.html',
                                        {'request': request,
                                        'app_name': settings.app_name,
                                        'news_list': finally_news_set,
                                        'user': user}
                                        )
