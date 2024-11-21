import asyncio
from datetime import timedelta, datetime

from celery import Celery
from celery.schedules import crontab

from sqlalchemy import select

from src.database import Session
from src.models.models import Secret

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

"""  Асинхронное извлечения секретов из базы данных, проверки
 их срока действия и удаления устаревших записей. Celery используется для 
 выполнения этой задачи в фоновом режиме"""


async def get_secret():
    async with Session() as session:
        query = select(Secret)
        result = await session.execute(query)
        secrets = result.fetchall()  # Получаем все записи
        for secret in secrets:
            yield secret


async def run_main():
    async with Session() as session:

        async for url_tuple in get_secret():
            url = url_tuple[0]

            url_in_current_session = await session.get(Secret, url.id)

            ttl = timedelta(minutes=url.TTL)
            data_create = url.date_of_creation
            present_time = datetime.now()

            time_action = present_time - data_create  # Разница во времени
            if time_action > ttl:
                await session.delete(url_in_current_session)
                await session.commit()


@celery_app.task
def main():
    # Запускаем асинхронную функцию

    #  Функция возвращает текущий цикл событий.
    #  Если цикл событий еще не создан, он будет создан автоматически
    loop = asyncio.get_event_loop()

    #  Эта команда запускает асинхронную функцию run_main и блокирует
    #  выполнение до тех пор, пока эта функция не завершится.
    loop.run_until_complete(run_main())


celery_app.conf.beat_schedule = {
    'main': {
        'task': 'src.secret.tasks.main',
        'schedule': crontab(minute='*/3'),
    },
}
