import uvicorn
from fastapi import FastAPI

from app.controllers.ClientController import client_router
from app.controllers.ClientFavoriteController import client_favorite_router

app = FastAPI()

app.include_router(client_router)
app.include_router(client_favorite_router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, log_level='info')