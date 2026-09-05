from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.state import State
    from app.db.models.district import District
    from app.db.models.scheme_channel_partner import SchemeChannelPartner


class ChannelPartner(IdMixins, TimeMixins):
    __tablename__ = "channel_partners"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    partner_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state_id: Mapped[str] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
    )

    district_id: Mapped[str | None] = mapped_column(
        ForeignKey("districts.id"),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    state: Mapped["State"] = relationship(
        "State",
    )

    district: Mapped["District"] = relationship(
        "District",
        back_populates="channel_partners",
    )

    scheme_channel_partners: Mapped[list["SchemeChannelPartner"]] = relationship(
        "SchemeChannelPartner",
        back_populates="channel_partner",
    )