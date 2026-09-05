from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.scheme import Scheme


class SchemeRepaymentRule(IdMixins, TimeMixins):
    __tablename__ = "scheme_repayment_rules"

    scheme_id: Mapped[str] = mapped_column(
        ForeignKey("schemes.id"),
        nullable=False,
    )

    repayment_frequency: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    max_repayment_period: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    moratorium_period: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    condition: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    scheme: Mapped["Scheme"] = relationship(
        "Scheme",
        back_populates="repayment_rules",
    )