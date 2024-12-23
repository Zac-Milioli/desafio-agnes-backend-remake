"Registro do model para activity"

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from .table_registry import table_registry


@table_registry.mapped_as_dataclass
class ActivityModel:
    "Modelo para Activity"
    __tablename__ = "activity"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), init=True)
    name: Mapped[str] = mapped_column(init=True, unique=True)
    status: Mapped[str] = mapped_column(init=True)
    description: Mapped[str] = mapped_column(init=True, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
