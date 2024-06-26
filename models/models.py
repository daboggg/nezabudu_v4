from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class User(Base):

    id: Mapped[int]
    username: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    delay_times: Mapped[str]
    auto_delay_time: Mapped[str]
    reminder_completed: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
