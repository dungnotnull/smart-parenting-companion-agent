from datetime import date, timedelta
from typing import Optional

from dateutil.relativedelta import relativedelta

from backend.services.age_stage_mapper import AgeStage, get_age_stage, WHO_MILESTONES

MILESTONE_UPPER_BOUNDS: dict[str, int] = {
    "Responds to sound": 3,
    "Rooting and sucking reflexes intact": 1,
    "Focuses on faces within 8-12 inches": 3,
    "Startle reflex (Moro) present": 4,
    "Rolls over (both directions by ~6m)": 7,
    "Sits without support (~6-8m)": 9,
    "Crawls (~7-10m)": 11,
    "Pulls to stand (~9-12m)": 13,
    "First words (~12m)": 15,
    "Pincer grasp (~10-12m)": 14,
    "Stranger anxiety emerges (~8-10m)": 11,
    "Walks independently (~12-15m)": 18,
    "Climbs stairs with help (~18-24m)": 26,
    "Uses 10-50 words (~18-24m)": 26,
    "Two-word phrases (~24m)": 28,
    "Pretend play emerges": 26,
    "Feeds self with spoon": 26,
    "Toilet training readiness (~24-36m)": 38,
    "Hops and balances on one foot (~4y)": 54,
    "Draws a person with 2-4 body parts": 54,
    "Engages in cooperative play": 54,
    "Follows 3-step commands": 54,
    "Tells simple stories": 54,
    "Counts to 10": 54,
    "Understands past/future concepts": 54,
    "Reads independently (~6-7y)": 90,
    "Understands conservation (Piaget stage)": 90,
    "Forms friendships with peers": 78,
    "Develops logical thinking": 90,
    "Understands rules and fairness": 90,
    "Increasing independence in self-care": 90,
    "Puberty onset changes": 180,
    "Abstract reasoning develops": 168,
    "Peer relationships intensify": 168,
    "Identity exploration begins": 192,
    "Mood variability increases": 168,
    "Advanced abstract reasoning": 228,
    "Future planning and goal-setting": 228,
    "Deeper intimate relationships": 228,
    "Moral/ethical reasoning matures": 228,
    "Career and life path exploration": 228,
    "Full cognitive maturity (frontal lobe ~25y)": 312,
    "Independent living skills": 264,
    "Career and relationship stability focus": 264,
}


def detect_milestone_delays(
    child_dob: date,
    logged_milestones: list[str],
    reference_date: Optional[date] = None,
) -> dict:
    ref = reference_date or date.today()
    stage, age_months = get_age_stage(child_dob, ref)
    expected_milestones = WHO_MILESTONES.get(stage, [])

    delays: list[dict] = []
    upcoming: list[dict] = []

    for milestone_label in expected_milestones:
        upper_bound = MILESTONE_UPPER_BOUNDS.get(milestone_label, age_months + 6)

        achieved = milestone_label in logged_milestones

        if achieved:
            continue

        if age_months > upper_bound:
            weeks_overdue = (age_months - upper_bound) * 4.345
            if weeks_overdue >= 4:
                delays.append({
                    "milestone": milestone_label,
                    "expected_by_months": upper_bound,
                    "current_age_months": age_months,
                    "weeks_overdue": round(weeks_overdue, 1),
                    "severity": "high" if weeks_overdue >= 12 else "moderate",
                })
        elif upper_bound - age_months <= 3:
            upcoming.append({
                "milestone": milestone_label,
                "expected_by_months": upper_bound,
                "current_age_months": age_months,
                "months_remaining": upper_bound - age_months,
            })

    has_concerns = len(delays) > 0

    return {
        "child_age_months": age_months,
        "developmental_stage": stage.value,
        "has_delays": has_concerns,
        "delays": delays,
        "upcoming_milestones": upcoming,
        "total_expected": len(expected_milestones),
        "total_achieved": len(logged_milestones),
        "total_delayed": len(delays),
        "recommendation": _generate_recommendation(has_concerns, delays),
    }


def _generate_recommendation(has_concerns: bool, delays: list[dict]) -> str:
    if not has_concerns:
        return "No significant milestone delays detected. Continue monitoring developmental progress at routine well-child visits."

    high_severity = [d for d in delays if d["severity"] == "high"]
    if high_severity:
        names = ", ".join(d["milestone"] for d in high_severity[:3])
        return (
            f"Several milestones appear significantly delayed: {names}. "
            "It is strongly recommended to schedule a developmental evaluation with your pediatrician. "
            "Early intervention services can make a substantial difference in outcomes. "
            "In the meantime, engage in activities that specifically target these skill areas."
        )

    names = ", ".join(d["milestone"] for d in delays[:3])
    return (
        f"Some milestones appear to be delayed: {names}. "
        "Discuss these observations at your next well-child visit. "
        "In the meantime, monitor progress and engage in supportive activities. "
        "Most children catch up with targeted support."
    )
