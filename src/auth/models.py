import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, UUIDMixin

if TYPE_CHECKING:
    from src.users.models import User


class RefreshToken(Base, UUIDMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    token: Mapped[str] = mapped_column(sa.String(500), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(sa.Boolean, default=False, server_default="false")

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
