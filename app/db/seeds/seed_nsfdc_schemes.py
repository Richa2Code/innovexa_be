from app.db.session import Session

from app.db.models.scheme import Scheme
from app.db.models.scheme_repayment_rule import SchemeRepaymentRule

from app.db.seeds.nsfdc_schemes import NSFDC_SCHEMES


def seed_nsfdc_schemes():
    db = Session()

    try:
        # ==========================================
        # 1. Create NSFDC Schemes
        # ==========================================
        for scheme_data in NSFDC_SCHEMES:

            # copy so the loop can run again (e.g. in tests) without
            # mutating the shared NSFDC_SCHEMES module-level list
            scheme_data = dict(scheme_data)
            repayment_rules_data = scheme_data.pop("repayment_rules", [])

            scheme = (
                db.query(Scheme)
                .filter(Scheme.name == scheme_data["name"])
                .first()
            )

            if not scheme:
                scheme = Scheme(**scheme_data)

                db.add(scheme)
                db.flush()

                print(f"Created scheme: {scheme_data['name']}")
            else:
                print(f"Scheme already exists: {scheme_data['name']}")

            # ======================================
            # 2. Create Repayment Rules
            # ======================================
            for rule_data in repayment_rules_data:

                existing_rule = (
                    db.query(SchemeRepaymentRule)
                    .filter(
                        SchemeRepaymentRule.scheme_id == scheme.id,
                        SchemeRepaymentRule.max_repayment_period
                        == rule_data["max_repayment_period"],
                        SchemeRepaymentRule.repayment_frequency
                        == rule_data["repayment_frequency"],
                    )
                    .first()
                )

                if not existing_rule:
                    rule = SchemeRepaymentRule(
                        scheme_id=scheme.id,
                        **rule_data,
                    )

                    db.add(rule)

                    print(
                        f"  Added repayment rule for {scheme_data['name']}: "
                        f"{rule_data['max_repayment_period']} "
                        f"({rule_data['repayment_frequency']})"
                    )
                else:
                    print(
                        f"  Repayment rule already exists for "
                        f"{scheme_data['name']}: "
                        f"{rule_data['max_repayment_period']}"
                    )

        db.commit()

        print("\n========================================")
        print("NSFDC scheme seeding completed successfully!")
        print(f"Schemes : {len(NSFDC_SCHEMES)}")
        print("========================================")

    except Exception as e:
        db.rollback()
        print(f"Error while seeding NSFDC schemes: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_nsfdc_schemes()