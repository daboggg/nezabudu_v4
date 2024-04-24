import json
import logging

from sqlalchemy import select, func, ChunkedIteratorResult, Result

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


# количество выполненных напоминаний (+1) для пользователя
async def reminder_completed(user_id: int) -> None:
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    user.reminder_completed += 1
    await session.commit()
    await session.close()


# общее количество выполненных напоминаний
async def all_reminder_completed() -> int:
    session = db_helper.get_session()
    query = select(func.sum(User.reminder_completed))
    result: ChunkedIteratorResult = await session.execute(query)
    await session.close()
    return result.scalar()


# взять всех пользователей из бд
async def get_users_from_db() -> list[User]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(User))
    tasks = result.scalars().all()
    await session.close()

    return list(tasks)


# взять пользователя из бд по id
async def get_user_from_db(user_id: int) -> User:
    session = db_helper.get_scoped_session()
    result = await session.execute(select(User).where(User.id == user_id))
    logger.info(f"получен reminder с id: {user_id}")
    result = result.scalar()
    await session.close()
    return result