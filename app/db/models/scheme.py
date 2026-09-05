from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.scheme_repayment_rule import SchemeRepaymentRule
    from app.db.models.scheme_channel_partner import SchemeChannelPartner


class Scheme(IdMixins, TimeMixins):
    __tablename__ = "schemes"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    purpose: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    min_project_cost: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    max_project_cost: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    finance_percentage: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    max_loan_amount: Mapped[float | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    nsfdc_interest_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    beneficiary_interest_rate: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    repayment_rules: Mapped[list["SchemeRepaymentRule"]] = relationship(
        "SchemeRepaymentRule",
        back_populates="scheme",
    )

    scheme_channel_partners: Mapped[list["SchemeChannelPartner"]] = relationship(
        "SchemeChannelPartner",
        back_populates="scheme",
    )