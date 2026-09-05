from app.db.session import Session

from app.db.models.scheme import Scheme
from app.db.models.scheme_repayment_rule import SchemeRepaymentRule
from app.db.models.channel_partner import ChannelPartner
from app.db.models.scheme_channel_partner import SchemeChannelPartner

from app.db.seeds.nsfdc_schemes import NSFDC_SCHEMES
from app.db.seeds.channel_partner_seed import seed_channel_partners


# ============================================================================
# Mapping: which ChannelPartner.partner_type values are eligible
# channelising institutions for each NSFDC scheme, per NSFDC's published
# scheme guidelines (https://nsfdc.nic.in/scheme):
#
#   - MFS & Term Loan          -> disbursed via State Channelising Agencies
#   - Aajeevika Micro-Finance  -> disbursed via NBFC-MFIs
#   - Udyam Nidhi Yojana       -> disbursed via Co-operative Banks/Societies
#                                 and Small Finance Banks
#   - Educational Loan Scheme  -> disbursed via SCAs, Public Sector Banks,
#                                 and Regional Rural Banks
#
# Scheme names below must match `name` in NSFDC_SCHEMES exactly.
# Partner types below must match `partner_type` in CHANNEL_PARTNERS exactly.
# ============================================================================
SCHEME_PARTNER_TYPE_MAP = {
    "Micro Finance Scheme (MFS)": [
        "State Channelising Agency",
    ],
    "Term Loan": [
        "State Channelising Agency",
    ],
    "Aajeevika Micro-Finance Yojana": [
        "NBFC-MFI",
    ],
    "Udyam Nidhi Yojana (UNY)": [
        "Co-operative Bank",
        "Cooperative Society",
        "Small Finance Bank",
    ],
    "Educational Loan Scheme (ELS)": [
        "State Channelising Agency",
        "Public Sector Bank",
        "Regional Rural Bank",
    ],
}


def seed_schemes_and_repayment_rules(db):
    """
    Seed Scheme rows and their SchemeRepaymentRule rows.
    Returns a dict of {scheme_name: Scheme instance} for use when
    creating SchemeChannelPartner links.
    """
    schemes_by_name = {}

    for scheme_data in NSFDC_SCHEMES:

        # copy so we don't mutate the shared NSFDC_SCHEMES list
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
                    f"  Added repayment rule: "
                    f"{rule_data['max_repayment_period']} "
                    f"({rule_data['repayment_frequency']})"
                )
            else:
                print(
                    f"  Repayment rule already exists: "
                    f"{rule_data['max_repayment_period']} "
                    f"({rule_data['repayment_frequency']})"
                )

        schemes_by_name[scheme_data["name"]] = scheme

    db.flush()

    return schemes_by_name


def seed_scheme_channel_partner_links(db, schemes_by_name):
    """
    Link each Scheme to every eligible ChannelPartner based on
    partner_type, per SCHEME_PARTNER_TYPE_MAP.
    Returns (links_created, links_already_existing).
    """
    links_created = 0
    links_existing = 0

    for scheme_name, partner_types in SCHEME_PARTNER_TYPE_MAP.items():

        scheme = schemes_by_name.get(scheme_name)

        if not scheme:
            print(f"  Scheme not found, skipping link step: {scheme_name}")
            continue

        partners = (
            db.query(ChannelPartner)
            .filter(ChannelPartner.partner_type.in_(partner_types))
            .all()
        )

        scheme_created = 0
        scheme_existing = 0

        for partner in partners:

            existing_link = (
                db.query(SchemeChannelPartner)
                .filter(
                    SchemeChannelPartner.scheme_id == scheme.id,
                    SchemeChannelPartner.channel_partner_id == partner.id,
                )
                .first()
            )

            if existing_link:
                scheme_existing += 1
                continue

            link = SchemeChannelPartner(
                scheme_id=scheme.id,
                channel_partner_id=partner.id,
            )

            db.add(link)
            scheme_created += 1

        links_created += scheme_created
        links_existing += scheme_existing

        print(
            f"  {scheme_name} <-> {partner_types}: "
            f"{len(partners)} eligible partner(s) found "
            f"({scheme_created} new links, {scheme_existing} already linked)"
        )

    return links_created, links_existing


def seed_nsfdc_full():
    # ==========================================
    # 1. Seed Channel Partners
    #
    # seed_channel_partners() manages its own Session, commit, and
    # close internally, so it is safe to call standalone before we
    # open our own session for schemes + links.
    # ==========================================
    print("========================================")
    print("STEP 1/3: Seeding Channel Partners")
    print("========================================")

    seed_channel_partners()

    # ==========================================
    # 2 & 3. Seed Schemes + Repayment Rules, then link to Partners
    # ==========================================
    db = Session()

    try:
        print("\n========================================")
        print("STEP 2/3: Seeding NSFDC Schemes + Repayment Rules")
        print("========================================")

        schemes_by_name = seed_schemes_and_repayment_rules(db)

        db.commit()

        print("\n========================================")
        print("STEP 3/3: Linking Schemes to Channel Partners")
        print("========================================")

        links_created, links_existing = seed_scheme_channel_partner_links(
            db,
            schemes_by_name,
        )

        db.commit()

        print("\n========================================")
        print("NSFDC full seeding completed successfully!")
        print("========================================")
        print(f"Schemes             : {len(NSFDC_SCHEMES)}")
        print(f"New partner links   : {links_created}")
        print(f"Existing links      : {links_existing}")
        print("========================================")

    except Exception as e:
        db.rollback()
        print(f"Error while seeding NSFDC schemes/links: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_nsfdc_full()