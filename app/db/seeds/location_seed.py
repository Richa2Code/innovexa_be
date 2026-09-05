
from app.db.session import Session

from app.db.models.country import Country
from app.db.models.state import State
from app.db.models.district import District

from app.db.seeds.india_locations import INDIA_DATA


def seed_locations():
    db = Session()

    try:
        # ==========================================
        # 1. Create India
        # ==========================================
        country = (
            db.query(Country)
            .filter(Country.code == "IN")
            .first()
        )

        if not country:
            country = Country(
                name="India",
                code="IN",
            )

            db.add(country)
            db.flush()

            print("Created country: India")
        else:
            print("Country already exists: India")

        # ==========================================
        # 2. Create States / Union Territories
        # ==========================================
        for state_name, district_names in INDIA_DATA.items():

            state = (
                db.query(State)
                .filter(
                    State.name == state_name,
                    State.country_id == country.id,
                )
                .first()
            )

            if not state:
                state = State(
                    name=state_name,
                    country_id=country.id,
                )

                db.add(state)
                db.flush()

                print(f"Created state/UT: {state_name}")
            else:
                print(f"State/UT already exists: {state_name}")

            # ======================================
            # 3. Create Districts
            # ======================================
            for district_name in district_names:

                district = (
                    db.query(District)
                    .filter(
                        District.name == district_name,
                        District.state_id == state.id,
                    )
                    .first()
                )

                if not district:
                    district = District(
                        name=district_name,
                        state_id=state.id,
                    )

                    db.add(district)

        db.commit()

        print("\n========================================")
        print("Location seeding completed successfully!")
        print("Country : India")
        print(f"States/UTs : {len(INDIA_DATA)}")
        print("========================================")

    except Exception as e:
        db.rollback()
        print(f"Error while seeding locations: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_locations()