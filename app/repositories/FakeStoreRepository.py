import requests
from typing import Optional
from app.config.Config import Config
from app.models.Models import ClientFavoriteModel

class FakeStoreRepository:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = Config().PRODUCT_API_URL

    def get_by_product_id(self, product_id: int) -> Optional[ClientFavoriteModel]:
        return self.session.get(f'{self.base_url}/products/{product_id}')
    
    def get_all_products(self) -> Optional[ClientFavoriteModel]:
        return self.session.get(f'{self.base_url}/products')
    
def get_fake_store_repository() -> FakeStoreRepository:
    return FakeStoreRepository()
