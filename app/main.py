import uvicorn
from fastapi import FastAPI

from app.controllers.AuthController import auth_router
from app.controllers.ClientController import client_router
from app.controllers.ProductsController import products_router
from app.controllers.ClientFavoriteController import client_favorite_router

app = FastAPI(
    title="AiQFome API",
    description="API para gerenciar clientes e produtos favoritos",
    version="1.0.0"    
)

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(products_router)
app.include_router(client_favorite_router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, log_level='info')
