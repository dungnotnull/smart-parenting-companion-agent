from datetime import date
from enum import Enum
from typing import TypedDict

from dateutil.relativedelta import relativedelta


class AgeStage(str, Enum):
    NEWBORN = "newborn"
    INFANT = "infant"
    TODDLER = "toddler"
    PRESCHOOL = "preschool"
    SCHOOL_AGE = "school-age"
    EARLY_ADOLESCENT = "early-adolescent"
    LATE_ADOLESCENT = "late-adolescent"
    ADULT = "adult"


WHO_MILESTONES: dict[AgeStage, list[str]] = {
    AgeStage.NEWBORN: [
        "Responds to sound",
        "Rooting and sucking reflexes intact",
        "Focuses on faces within 8-12 inches",
        "Startle reflex (Moro) present",
    ],
    AgeStage.INFANT: [
        "Rolls over (both directions by ~6m)",
        "Sits without support (~6-8m)",
        "Crawls (~7-10m)",
        "Pulls to stand (~9-12m)",
        "First words (~12m)",
        "Pincer grasp (~10-12m)",
        "Stranger anxiety emerges (~8-10m)",
    ],
    AgeStage.TODDLER: [
        "Walks independently (~12-15m)",
        "Climbs stairs with help (~18-24m)",
        "Uses 10-50 words (~18-24m)",
        "Two-word phrases (~24m)",
        "Pretend play emerges",
        "Feeds self with spoon",
        "Toilet training readiness (~24-36m)",
    ],
    AgeStage.PRESCHOOL: [
        "Hops and balances on one foot (~4y)",
        "Draws a person with 2-4 body parts",
        "Engages in cooperative play",
        "Follows 3-step commands",
        "Tells simple stories",
        "Counts to 10",
        "Understands past/future concepts",
    ],
    AgeStage.SCHOOL_AGE: [
        "Reads independently (~6-7y)",
        "Understands conservation (Piaget stage)",
        "Forms friendships with peers",
        "Develops logical thinking",
        "Understands rules and fairness",
        "Increasing independence in self-care",
    ],
    AgeStage.EARLY_ADOLESCENT: [
        "Puberty onset changes",
        "Abstract reasoning develops",
        "Peer relationships intensify",
        "Identity exploration begins",
        "Mood variability increases",
    ],
    AgeStage.LATE_ADOLESCENT: [
        "Advanced abstract reasoning",
        "Future planning and goal-setting",
        "Deeper intimate relationships",
        "Moral/ethical reasoning matures",
        "Career and life path exploration",
    ],
    AgeStage.ADULT: [
        "Full cognitive maturity (frontal lobe ~25y)",
        "Independent living skills",
        "Career and relationship stability focus",
    ],
}

ERIKSON_STAGE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: "Trust vs. Mistrust (0-18 months)",
    AgeStage.INFANT: "Trust vs. Mistrust → Autonomy vs. Shame/Doubt (18m-3y)",
    AgeStage.TODDLER: "Autonomy vs. Shame/Doubt (18 months-3 years)",
    AgeStage.PRESCHOOL: "Initiative vs. Guilt (3-5 years)",
    AgeStage.SCHOOL_AGE: "Industry vs. Inferiority (6-11 years)",
    AgeStage.EARLY_ADOLESCENT: "Identity vs. Role Confusion (12-18 years)",
    AgeStage.LATE_ADOLESCENT: "Identity vs. Role Confusion → Intimacy vs. Isolation",
    AgeStage.ADULT: "Intimacy vs. Isolation (young adulthood)",
}

PIAGET_STAGE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: "Sensorimotor (0-2 years)",
    AgeStage.INFANT: "Sensorimotor (0-2 years)",
    AgeStage.TODDLER: "Sensorimotor → Preoperational (2-7 years)",
    AgeStage.PRESCHOOL: "Preoperational (2-7 years)",
    AgeStage.SCHOOL_AGE: "Concrete Operational (7-11 years)",
    AgeStage.EARLY_ADOLESCENT: "Formal Operational (12+ years)",
    AgeStage.LATE_ADOLESCENT: "Formal Operational (12+ years)",
    AgeStage.ADULT: "Formal Operational (12+ years)",
}


class DevelopmentalContext(TypedDict):
    stage: str
    age_months: int
    erikson_stage: str
    piaget_stage: str
    key_milestones: list[str]
    stage_guidance: str


STAGE_GUIDANCE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: (
        "Focus on responsive caregiving, establishing feeding and sleep rhythms, "
        "skin-to-skin contact, and recognizing newborn cues. Parents should prioritize "
        "postpartum recovery and mental health."
    ),
    AgeStage.INFANT: (
        "Encourage floor play, tummy time, responsive feeding (breast or formula), "
        "introduction of complementary foods at 6 months, and safe sleep practices. "
        "Parent-child attachment is the primary developmental driver."
    ),
    AgeStage.TODDLER: (
        "Support autonomy within safe boundaries. Use positive discipline and redirection "
        "rather than punishment. Language-rich environment is crucial. Consistent routines "
        "reduce power struggles."
    ),
    AgeStage.PRESCHOOL: (
        "Encourage curiosity, imaginative play, and early social skills. Set clear limits "
        "with warmth. School readiness includes self-regulation more than academic skills. "
        "Monitor peer interactions."
    ),
    AgeStage.SCHOOL_AGE: (
        "Support academic growth while preserving intrinsic motivation. Balance structure "
        "with free play. Coach friendship and conflict resolution skills. Monitor screen time "
        "quality and quantity."
    ),
    AgeStage.EARLY_ADOLESCENT: (
        "Respect growing autonomy while maintaining connection. Listen more than lecture. "
        "Support identity exploration. Monitor mental health (depression, anxiety red flags). "
        "Discuss puberty changes openly and positively."
    ),
    AgeStage.LATE_ADOLESCENT: (
        "Shift from managing to coaching/consulting. Support future planning while allowing "
        "the adolescent to lead. Respect privacy. Continue monitoring mental health. "
        "Discuss risk-taking within a harm-reduction framework."
    ),
    AgeStage.ADULT: (
        "Provide resources and support when requested. Respect autonomy fully. "
        "Focus on transition-to-adulthood challenges: finances, career, relationships."
    ),
}


def get_age_stage(dob: date, reference_date: date | None = None) -> tuple[AgeStage, int]:
    ref = reference_date or date.today()
    delta = relativedelta(ref, dob)
    age_months = delta.years * 12 + delta.months + (1 if delta.days >= 15 else 0)

    if age_months < 1:
        stage = AgeStage.NEWBORN
    elif age_months < 12:
        stage = AgeStage.INFANT
    elif age_months < 36:
        stage = AgeStage.TODDLER
    elif age_months < 60:
        stage = AgeStage.PRESCHOOL
    elif age_months < 144:
        stage = AgeStage.SCHOOL_AGE
    elif age_months < 192:
        stage = AgeStage.EARLY_ADOLESCENT
    elif age_months < 264:
        stage = AgeStage.LATE_ADOLESCENT
    else:
        stage = AgeStage.ADULT

    return stage, age_months


def get_developmental_context(dob: date, reference_date: date | None = None) -> DevelopmentalContext:
    stage, age_months = get_age_stage(dob, reference_date)
    return {
        "stage": stage.value,
        "age_months": age_months,
        "erikson_stage": ERIKSON_STAGE.get(stage, "Unknown"),
        "piaget_stage": PIAGET_STAGE.get(stage, "Unknown"),
        "key_milestones": WHO_MILESTONES.get(stage, []),
        "stage_guidance": STAGE_GUIDANCE.get(stage, ""),
    }
