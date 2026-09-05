from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.country import Country
    from app.db.models.district import District


class State(IdMixins, TimeMixins):
    __tablename__ = "states"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    country_id: Mapped[str] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="states",
    )

    districts: Mapped[list["District"]] = relationship(
        "District",
        back_populates="state",
    )