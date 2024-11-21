import uuid

from pydantic import BaseModel


class CreateSecret(BaseModel):
    secret: str
    code_phrase: str
    TTL: int


class SecretResponse(BaseModel):

    secret_key: str
