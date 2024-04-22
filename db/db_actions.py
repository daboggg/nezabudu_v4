import json
import logging

from sqlalchemy import select

from db.db_helper import db_helper
from models import User

logger = logging.getLogger(__name__)


# добавляет пользователя в бд
async def add_user_to_db(user_id: int, username: str, first_name: str, last_name: str) -> None:
    session = db_helper.get_scoped_session()
    user: User = (await session.execute(select(User).where(User.id == user_id))).scalar()

    if not user:
        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            delay_times='''["('minutes', 10, '10 мин')"]''',
            auto_delay_time='{"minutes": 15}',
        )
        session.add(user)
        await session.commit()
    await session.close()


# добавить авто откладывание напоминания
async def set_auto_delay_time(user_id: int, auto_delay_time: dict) -> None:
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    user.auto_delay_time = json.dumps(auto_delay_time)
    await session.commit()
    await session.close()


# получить авто откладывание напоминания
async def get_auto_delay_time(user_id: int) -> str:
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    auto_delay_time = user.auto_delay_time
    await session.close()
    return auto_delay_time


# добавить откладывания напоминания
async def set_delay_times(user_id: int, delay_times: str) -> None:
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    user.delay_times = delay_times
    await session.commit()
    await session.close()


# получить набор для кнопок откладывания напоминания
async def get_delay_times(user_id: int) -> str:
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    delay_times = user.delay_times
    await session.close()
    return delay_times
