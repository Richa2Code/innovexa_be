from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import IdMixins, TimeMixins

if TYPE_CHECKING:
    from app.db.models.scheme import Scheme
    from app.db.models.channel_partner import ChannelPartner


class SchemeChannelPartner(IdMixins, TimeMixins):
    __tablename__ = "scheme_channel_partners"

    scheme_id: Mapped[str] = mapped_column(
        ForeignKey("schemes.id"),
        nullable=False,
    )

    channel_partner_id: Mapped[str] = mapped_column(
        ForeignKey("channel_partners.id"),
        nullable=False,
    )

    scheme: Mapped["Scheme"] = relationship(
        "Scheme",
        back_populates="scheme_channel_partners",
    )

    channel_partner: Mapped["ChannelPartner"] = relationship(
        "ChannelPartner",
        back_populates="scheme_channel_partners",
    )