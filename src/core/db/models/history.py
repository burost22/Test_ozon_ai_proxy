from datetime import UTC
from datetime import datetime as dt

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import (Mapped, declarative_base, declared_attr,
                            mapped_column)


class PreBase:

    @declared_attr
    def __tablename__(cls):  # noqa: N805
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[dt] = mapped_column(
        DateTime(timezone=True), nullable=False, default=dt.now(UTC)
    )


Base = declarative_base(cls=PreBase)


class HistoryModel(Base):
    """Модель историй запросов"""

    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return (f"История по запросу - {self.question}"
                f" c id - {self.id} и ответом - {self.answer}"
                f", время создания - {self.timestamp}"
        )
