from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.state import State
    from app.db.models.channel_partner import ChannelPartner


class District(IdMixins, TimeMixins):
    __tablename__ = "districts"

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    state_id: Mapped[str] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
    )

    state: Mapped["State"] = relationship(
        "State",
        back_populates="districts",
    )

    channel_partners: Mapped[list["ChannelPartner"]] = relationship(
        "ChannelPartner",
        back_populates="district",
    )