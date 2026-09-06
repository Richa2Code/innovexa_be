"""
Seed latitude and longitude for all channel partners.

Reads coordinates from:
    channel_partner_coordinates.py

Updates:
    ChannelPartner.latitude
    ChannelPartner.longitude

Run from project root:
    python -m app.db.seeds.seed_channel_partner_coordinates
"""

from app.db.session import Session
from app.db.models.channel_partner import ChannelPartner

from app.db.seeds.channel_partner_coordinates import (
    CHANNEL_PARTNER_COORDINATES,
)


def seed_channel_partner_coordinates():
    db = Session()

    try:
        updated = 0
        not_found = 0

        print("=" * 70)
        print("INNOVEXA - CHANNEL PARTNER COORDINATES SEEDER")
        print("=" * 70)

        print(
            f"Coordinate records available: "
            f"{len(CHANNEL_PARTNER_COORDINATES)}"
        )

        print()

        for name, coordinates in CHANNEL_PARTNER_COORDINATES.items():

            partner = (
                db.query(ChannelPartner)
                .filter(ChannelPartner.name == name)
                .first()
            )

            if not partner:
                print(f"[NOT FOUND] {name}")
                not_found += 1
                continue

            latitude = coordinates.get("latitude")
            longitude = coordinates.get("longitude")

            if latitude is None or longitude is None:
                print(f"[SKIPPED] {name} -> coordinates missing")
                continue

            partner.latitude = latitude
            partner.longitude = longitude

            updated += 1

            print(
                f"[UPDATED] {name}"
                f" -> {latitude}, {longitude}"
            )

        db.commit()

        print()
        print("=" * 70)
        print("CHANNEL PARTNER COORDINATES SEEDING COMPLETED")
        print("=" * 70)
        print(f"Coordinate records : {len(CHANNEL_PARTNER_COORDINATES)}")
        print(f"Updated            : {updated}")
        print(f"Not found in DB    : {not_found}")
        print("=" * 70)

    except Exception as e:
        db.rollback()

        print()
        print("=" * 70)
        print("ERROR WHILE SEEDING CHANNEL PARTNER COORDINATES")
        print("=" * 70)
        print(e)
        print("=" * 70)

        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_channel_partner_coordinates()