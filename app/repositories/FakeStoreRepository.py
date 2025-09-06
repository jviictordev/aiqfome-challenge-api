import requests
from typing import Optional
from app.models.Models import ClientFavoriteModel

class FakeStoreRepository:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://fakestoreapi.com'

    def get_by_product_id(self, product_id: int) -> Optional[ClientFavoriteModel]:
        return self.session.get(f'{self.base_url}/products/{product_id}')
    
def get_fake_store_repository() -> FakeStoreRepository:
    return FakeStoreRepository()
