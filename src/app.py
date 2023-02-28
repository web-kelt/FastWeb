from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
app.mount('/static', StaticFiles(directory='src/static'), name='static')
templates = Jinja2Templates(directory='src/templates')

from src.routes import home

