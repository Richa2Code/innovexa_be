"""
Generate a separate channel_partner_coordinates.py file.

Place this file in:
    app/db/seeds/geocode_channel_partners.py

Run from the project root:
    python -m app.db.seeds.geocode_channel_partners

Requirements:
    pip install geopy

This script:
- reads CHANNEL_PARTNERS from channel_partners.py
- tries ArcGIS first (usually better for Indian addresses)
- falls back to Nominatim
- tries several address variations
- DOES NOT modify your database
- creates:
    app/db/seeds/channel_partner_coordinates.py
    app/db/seeds/channel_partner_geocoding_failed.json
    app/db/seeds/channel_partner_geocoding_review.json
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from geopy.geocoders import ArcGIS, Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut

from app.db.seeds.channel_partner_seed import CHANNEL_PARTNERS


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "channel_partner_coordinates.py"
FAILED_FILE = BASE_DIR / "channel_partner_geocoding_failed.json"
REVIEW_FILE = BASE_DIR / "channel_partner_geocoding_review.json"

# Keep requests slow enough for public geocoders.
REQUEST_DELAY = 1.5

arcgis = ArcGIS(timeout=20)
nominatim = Nominatim(user_agent="innovexa-sih-2026-channel-partners", timeout=20)


def clean(value):
    if value is None:
        return ""
    return " ".join(str(value).replace("\n", " ").split())


def normalize_pincode(value):
    value = clean(value)
    # Fix malformed values such as "400" by not pretending they are valid PINs.
    return value if re.fullmatch(r"\d{6}", value) else ""


def build_queries(data):
    name = clean(data.get("name"))
    address = clean(data.get("address"))
    district = clean(data.get("district"))
    state = clean(data.get("state"))
    pincode = normalize_pincode(data.get("pincode"))

    queries = []

    # Most specific first.
    if address and pincode:
        queries.append(f"{address}, {pincode}, India")

    if address and district and state:
        queries.append(f"{address}, {district}, {state}, India")

    if name and address and district and state:
        queries.append(f"{name}, {address}, {district}, {state}, India")

    if name and district and state and pincode:
        queries.append(f"{name}, {district}, {state}, {pincode}, India")

    if name and district and state:
        queries.append(f"{name}, {district}, {state}, India")

    if address and state:
        queries.append(f"{address}, {state}, India")

    # Remove duplicates while preserving order.
    result = []
    seen = set()
    for query in queries:
        query = clean(query)
        if query and query.lower() not in seen:
            seen.add(query.lower())
            result.append(query)

    return result


def looks_india(result):
    if not result:
        return False

    text = clean(getattr(result, "address", "")).lower()
    return (
        "india" in text
        or "bharat" in text
        or ", in" in text
    )


def geocode_one(data):
    queries = build_queries(data)

    # ---------- ARC GIS ----------
    for query in queries:
        try:
            result = arcgis.geocode(query)
            time.sleep(REQUEST_DELAY)

            if result and getattr(result, "latitude", None) is not None:
                return {
                    "latitude": float(result.latitude),
                    "longitude": float(result.longitude),
                    "provider": "ArcGIS",
                    "query": query,
                    "matched_address": clean(getattr(result, "address", "")),
                }

        except (GeocoderTimedOut, GeocoderServiceError, Exception):
            # Try the next query/provider.
            pass

    # ---------- NOMINATIM ----------
    for query in queries:
        try:
            result = nominatim.geocode(
                query,
                country_codes="in",
                addressdetails=True,
            )
            time.sleep(REQUEST_DELAY)

            if result and getattr(result, "latitude", None) is not None:
                if looks_india(result):
                    return {
                        "latitude": float(result.latitude),
                        "longitude": float(result.longitude),
                        "provider": "Nominatim",
                        "query": query,
                        "matched_address": clean(getattr(result, "address", "")),
                    }

        except (GeocoderTimedOut, GeocoderServiceError, Exception):
            pass

    return None


def write_coordinates(records):
    lines = [
        '"""Auto-generated channel partner coordinates."""',
        "",
        "CHANNEL_PARTNER_COORDINATES = {",
    ]

    for name in sorted(records):
        item = records[name]
        lines.append(f"    {name!r}: {{")
        lines.append(f"        'latitude': {item['latitude']!r},")
        lines.append(f"        'longitude': {item['longitude']!r},")
        lines.append("    },")

    lines.extend([
        "}",
        "",
    ])

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    coordinates = {}
    failed = []
    review = []

    total = len(CHANNEL_PARTNERS)

    print("=" * 70)
    print("Innovexa - Channel Partner Geocoder")
    print("=" * 70)
    print(f"Total records: {total}")
    print("Provider order: ArcGIS -> Nominatim")
    print()

    for index, data in enumerate(CHANNEL_PARTNERS, start=1):
        name = clean(data.get("name"))

        print(f"[{index}/{total}] {name}")

        # Records with no usable address cannot be accurately geocoded.
        if not clean(data.get("address")) and not data.get("pincode"):
            failed.append({
                "name": name,
                "reason": "No office address or valid PIN supplied",
            })
            print("    SKIPPED: no usable address")
            continue

        result = geocode_one(data)

        if result:
            coordinates[name] = {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
            }

            # Keep metadata separately so the static coordinate file stays clean.
            review.append({
                "name": name,
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "provider": result["provider"],
                "query": result["query"],
                "matched_address": result["matched_address"],
            })

            print(
                f"    FOUND: {result['latitude']}, {result['longitude']}"
            )
            print(f"    via {result['provider']}")
            print(f"    matched: {result['matched_address']}")
        else:
            failed.append({
                "name": name,
                "state": data.get("state"),
                "district": data.get("district"),
                "address": data.get("address"),
                "pincode": data.get("pincode"),
            })
            print("    NOT FOUND")

        # Save progress after every record.
        write_coordinates(coordinates)
        FAILED_FILE.write_text(
            json.dumps(failed, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        REVIEW_FILE.write_text(
            json.dumps(review, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    print(f"Found       : {len(coordinates)}")
    print(f"Not found   : {len(failed)}")
    print(f"Coordinate file: {OUTPUT_FILE}")
    print(f"Failed file    : {FAILED_FILE}")
    print(f"Review file    : {REVIEW_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
