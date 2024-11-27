from shutil import which
from cryptography.fernet import Fernet
# import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession as As
from datetime import datetime, timedelta
from src.database import get_async_session, Session
from src.models.models import Secret
from src.secret.shema import CreateSecret, SecretResponse

router = APIRouter(
    prefix="/generate",
    tags=["Generate"]
)


# def hash_secret_code_phrase(data: str) -> str:
#     # Хешируем secret и code
#     hashed = bcrypt.hashpw(data.encode('utf-8'), bcrypt.gensalt())
#     return hashed.decode('utf-8')
#
#
# def check_code_phrase(code_phrase: str, hashed_code_phrase: str) -> bool:
#     # Проверяем секретный код
#     return bcrypt.checkpw(code_phrase.encode('utf-8'),
#                           hashed_code_phrase.encode('utf-8'))


@router.post("/", response_model=SecretResponse)
async def generate(car: CreateSecret,
                   session: As = Depends(get_async_session)):
    """
        Generate a new secret.

        - **secret**: The secret string to be encrypted.
        - **code_phrase**: The code phrase used for encryption.
        - **TTL**: Time to live for the secret.
    """

    try:
        secret_key = Fernet.generate_key()

        key = secret_key  # Замените на ваш фактический ключ
        fernet = Fernet(key)

        secret = car.secret
        encrypted_secret_key = fernet.encrypt(secret.encode())

        code_phrase = car.code_phrase
        encrypted_code_phrase = fernet.encrypt(code_phrase.encode())

        new_car = Secret(secret=encrypted_secret_key.decode('utf-8'),
                         secret_key=secret_key.decode('utf-8'),
                         code_phrase=encrypted_code_phrase.decode('utf-8'),

                         TTL=car.TTL)
        session.add(new_car)
        await session.commit()

        secret_key = new_car.secret_key

        return SecretResponse(

            secret_key=secret_key
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=500,
                            detail={"error": "Ошибка базы данных"})


@router.get("/{secret_key}")
async def get_secret(secret_key: str,
                     session: As = Depends(get_async_session)):
    """
        Retrieve a secret by its key.

        - **secret_key**: The key of the secret to retrieve.
    """

    try:

        query = select(Secret.secret, Secret.code_phrase).filter(
            Secret.secret_key == secret_key)

        result = await session.execute(query)

        # Получение первой строки результата
        secret_data = result.fetchone()

        if secret_data is None:
            raise HTTPException(status_code=404, detail="Secret not found")

        secret, code = secret_data  # Извлекаем secret

        # secret_key преобразуем в байтовый тип для передачи ключа
        # для расшифровки секрета
        secret_key_bytes = secret_key.encode('utf-8')
        secret = secret.encode('utf-8')

        key = secret_key_bytes  # Замените на ваш фактический ключ
        fernet = Fernet(key)

        # Расшифровка секрета
        decrypted_secret = fernet.decrypt(secret).decode()
        return {"secret": decrypted_secret}
    except SQLAlchemyError:

        raise HTTPException(status_code=500,
                            detail={"error": "Ошибка базы данных"})
