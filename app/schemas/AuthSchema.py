from pydantic import BaseModel

class AuthSchema(BaseModel):
    access_token: str
    token_type: str