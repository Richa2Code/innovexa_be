from typing import Dict, Any, List, Optional
from app.db.models.scheme import Scheme
from app.schema.public import SchemeEligibilityRequest, ScoreBreakdown


class AIEligibilityEngine:
    """
    3-Layer AI Intelligence System:
    1. Rule-Based Eligibility Engine: Hard rule checking (Income, project cost bounds, category, location).
    2. Scheme Matching & Ranking Algorithm: Multi-criteria weighted scoring algorithm (100-point scale).
       - Purpose Match: 40 points
       - Income Match: 25 points
       - Project Cost Match: 25 points
       - Location & Other Criteria: 10 points
    3. Explainable Recommendation System: Generates human-readable justification for scores.
    """

    MAX_PURPOSE_SCORE = 40.0
    MAX_INCOME_SCORE = 25.0
    MAX_PROJECT_COST_SCORE = 25.0
    MAX_LOCATION_SCORE = 10.0

    @classmethod
    def evaluate_scheme(
        cls,
        scheme: Scheme,
        user_request: SchemeEligibilityRequest,
        has_location_match: bool = False,
    ) -> Dict[str, Any]:
        # Layer 1: Eligibility check (Hard rules)
        is_eligible, eligibility_reason = cls._check_hard_eligibility(scheme, user_request)
        if not is_eligible:
            return {
                "is_eligible": False,
                "suitability_score": 0.0,
                "suitability_label": "Ineligible",
                "recommendation_reason": eligibility_reason,
                "score_breakdown": ScoreBreakdown(
                    purpose_score=0.0,
                    income_score=0.0,
                    project_cost_score=0.0,
                    location_score=0.0,
                ),
            }

        # Layer 2: Scoring & Ranking Algorithm
        purpose_score, purpose_reason = cls._score_purpose(scheme, user_request.purpose)
        income_score, income_reason = cls._score_income(user_request.annual_income)
        cost_score, cost_reason = cls._score_project_cost(scheme, user_request.project_cost)
        location_score, location_reason = cls._score_location(has_location_match, user_request.state_id, user_request.district_id)

        total_score = round(purpose_score + income_score + cost_score + location_score, 1)

        label = cls._get_suitability_label(total_score)

        # Layer 3: Explainable Recommendation
        reasons = [r for r in [purpose_reason, income_reason, cost_reason, location_reason] if r]
        recommendation_reason = "; ".join(reasons) + "."

        breakdown = ScoreBreakdown(
            purpose_score=round(purpose_score, 1),
            income_score=round(income_score, 1),
            project_cost_score=round(cost_score, 1),
            location_score=round(location_score, 1),
        )

        return {
            "is_eligible": True,
            "suitability_score": total_score,
            "suitability_label": label,
            "recommendation_reason": recommendation_reason,
            "score_breakdown": breakdown,
        }

    @classmethod
    def _check_hard_eligibility(cls, scheme: Scheme, req: SchemeEligibilityRequest) -> tuple[bool, str]:
        annual_income = (req.annual_income) if req.annual_income is not None else None
        project_cost = (req.project_cost) if req.project_cost is not None else None
        min_project_cost = float(scheme.min_project_cost) if scheme.min_project_cost is not None else None
        max_project_cost = float(scheme.max_project_cost) if scheme.max_project_cost is not None else None

        # Hard Rule 1: Annual Income threshold (Max eligibility limit: ₹5,00,000 / ₹5 Lakhs)
        if annual_income is not None and annual_income > 500000:
            return False, "Annual income exceeds maximum eligible limit of ₹5,00,000 (₹5 Lakhs) for scheme eligibility."

        # Hard Rule 2: Minimum Project Cost
        if project_cost is not None and min_project_cost is not None:
            if project_cost < min_project_cost:
                return False, f"Project cost (₹{project_cost:,.0f}) is below scheme minimum threshold (₹{min_project_cost:,.0f})."

        # Hard Rule 3: Maximum Project Cost
        if project_cost is not None and max_project_cost is not None:
            if project_cost > max_project_cost:
                return False, f"Project cost (₹{project_cost:,.0f}) exceeds scheme maximum limit (₹{max_project_cost:,.0f})."

        return True, ""

    @classmethod
    def _score_purpose(cls, scheme: Scheme, purpose: Optional[str]) -> tuple[float, str]:
        if not purpose:
            return 25.0, "General purpose scheme match"

        user_purpose_lower = purpose.strip().lower()
        scheme_purpose_lower = (scheme.purpose or "").lower()
        scheme_name_lower = (scheme.name or "").lower()
        scheme_cat_lower = (scheme.category or "").lower()

        # Direct purpose match
        if user_purpose_lower in scheme_purpose_lower or user_purpose_lower in scheme_name_lower or user_purpose_lower in scheme_cat_lower:
            return cls.MAX_PURPOSE_SCORE, f"High relevance for '{purpose}'"
        
        # Token / Partial match
        user_tokens = set(user_purpose_lower.split())
        scheme_tokens = set(f"{scheme_purpose_lower} {scheme_name_lower} {scheme_cat_lower}".split())
        matched_tokens = user_tokens.intersection(scheme_tokens)

        if matched_tokens:
            return 30.0, f"Partial purpose match for '{purpose}'"

        return 15.0, f"Applicable for multi-purpose activities including '{purpose}'"

    @classmethod
    def _score_income(cls, annual_income: Optional[float]) -> tuple[float, str]:
        if annual_income is None:
            return 18.0, "Income criteria verified"

        income_val = float(annual_income)
        # Lower income tiers receive higher suitability score in government assistance schemes
        if income_val <= 150000:
            return cls.MAX_INCOME_SCORE, f"Priority financial tier (Income ₹{income_val:,.0f})"
        elif income_val <= 300000:
            return 22.5, f"Highly eligible income bracket (Income ₹{income_val:,.0f})"
        elif income_val <= 600000:
            return 20.0, f"Standard eligible income tier (Income ₹{income_val:,.0f})"
        else:
            return 15.0, f"Eligible income tier (Income ₹{income_val:,.0f})"

    @classmethod
    def _score_project_cost(cls, scheme: Scheme, project_cost: Optional[float]) -> tuple[float, str]:
        if project_cost is None:
            return 18.0, "Project cost within standard range"

        cost_val = float(project_cost)
        min_c = float(scheme.min_project_cost) if scheme.min_project_cost is not None else 0.0
        max_c = float(scheme.max_project_cost) if scheme.max_project_cost is not None else None

        if max_c and max_c > min_c:
            mid_point = (min_c + max_c) / 2.0
            distance_from_mid = abs(cost_val - mid_point) / (max_c - min_c)
            score = max(10.0, float(cls.MAX_PROJECT_COST_SCORE) * (1.0 - (distance_from_mid * 0.5)))
            return score, f"Project cost ₹{cost_val:,.0f} fits scheme cost range (₹{min_c:,.0f} - ₹{max_c:,.0f})"
        elif max_c:
            return 22.0, f"Project cost ₹{cost_val:,.0f} within scheme max cap of ₹{max_c:,.0f}"
        else:
            return 20.0, f"Project cost ₹{cost_val:,.0f} is covered under scheme guidelines"

    @classmethod
    def _score_location(cls, has_location_match: bool, state_id: Optional[str], district_id: Optional[str]) -> tuple[float, str]:
        if district_id and has_location_match:
            return cls.MAX_LOCATION_SCORE, "Direct channel partner availability in user district"
        elif state_id and has_location_match:
            return 8.0, "Channel partner operational in user state"
        else:
            return 5.0, "Nationwide/Statewide implementation partner coverage"

    @classmethod
    def _get_suitability_label(cls, score: float) -> str:
        if score >= 85.0:
            return "Highly Suitable"
        elif score >= 70.0:
            return "Suitable"
        elif score >= 55.0:
            return "Moderately Suitable"
        else:
            return "Low Suitability"
