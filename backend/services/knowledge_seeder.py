import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from backend.services.embedding import get_embedding_service
from backend.services.knowledge_store import get_knowledge_store

logger = logging.getLogger(__name__)

SEED_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "seed_chunks.json"


def _generate_seed_chunks() -> list[dict]:
    chunks: list[dict] = []

    chunks.extend([
        {
            "id": "seed-aap-bright-futures-1",
            "text": "Bright Futures Guidelines for Health Supervision of Infants, Children, and Adolescents (4th Edition) recommends well-child visits at: newborn, 3-5 days, 1 month, 2 months, 4 months, 6 months, 9 months, 12 months, 15 months, 18 months, 24 months, 30 months, and annually from 3-21 years. Each visit includes: health history, physical examination, developmental surveillance, screening tests, immunizations, and anticipatory guidance tailored to the child's age.",
            "metadata": {"source": "AAP Bright Futures", "evidence_level": "guideline", "year": 2017, "age_stage": "all", "domain": "general-pediatrics"},
        },
        {
            "id": "seed-aap-bright-futures-2",
            "text": "AAP Bright Futures recommends developmental surveillance at every well-child visit using standardized tools. The Ages & Stages Questionnaire (ASQ-3) should be administered at 4, 6, 8, 10, 12, 18, 24, 30, 36, 48, and 60 months. Autism-specific screening (M-CHAT-R/F) is recommended at 18 and 24 months. If concerns arise, simultaneous referral to early intervention AND diagnostic evaluation is recommended — do not wait for diagnosis to initiate services.",
            "metadata": {"source": "AAP Bright Futures", "evidence_level": "guideline", "year": 2017, "age_stage": "infant", "domain": "development"},
        },
        {
            "id": "seed-aap-safe-sleep-1",
            "text": "AAP 2022 Safe Sleep Guidelines: (1) Place infants on their back to sleep for every sleep until 1 year of age. (2) Use a firm, flat, non-inclined sleep surface. (3) Room-share but do not bed-share for at least the first 6 months. (4) Keep soft objects, loose bedding, pillows, bumper pads, and toys out of the sleep area. (5) Avoid overheating and head covering. (6) Offer a pacifier at nap time and bedtime. (7) Avoid smoke, alcohol, and illicit drug exposure during pregnancy and after birth. (8) Supervised, awake tummy time is recommended to facilitate development and minimize positional plagiocephaly.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2022, "age_stage": "infant", "domain": "sleep"},
        },
        {
            "id": "seed-aap-safe-sleep-2",
            "text": "Meta-analysis of 15 case-control studies demonstrates that room-sharing without bed-sharing reduces SIDS risk by up to 50%. The protective effect is greatest in the first 6 months. Bed-sharing significantly increases SIDS risk (OR 2.89, 95% CI 1.99-4.18) especially when combined with parental smoking, alcohol consumption, or formula feeding. The AAP recommends a separate sleep surface in the parents' room for at least the first 6 months, optimally the first year.",
            "metadata": {"source": "Pediatrics", "evidence_level": "meta-analysis", "year": 2022, "age_stage": "infant", "domain": "sleep"},
        },
        {
            "id": "seed-who-feeding-1",
            "text": "WHO Infant and Young Child Feeding Guidelines: Exclusive breastfeeding is recommended for the first 6 months of life. Continued breastfeeding is recommended along with appropriate complementary foods up to 2 years of age or beyond. Complementary foods should be introduced at 6 months (180 days) while continuing to breastfeed. Foods should be: timely (introduced when energy needs exceed breast milk alone), adequate (sufficient energy, protein, micronutrients), safe (hygienically prepared and stored), and properly fed (responsive to hunger and satiety cues).",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2023, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-who-feeding-2",
            "text": "WHO recommends daily iron supplementation (10-12.5 mg elemental iron) for infants and young children aged 6-23 months in populations where anemia prevalence is ≥40%. In malaria-endemic areas, iron should be provided alongside malaria prevention and treatment services. Iron-rich complementary foods include: pureed meat, poultry, fish, liver, fortified infant cereals, and legumes. Vitamin C-rich foods enhance non-heme iron absorption when consumed in the same meal.",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2023, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-aap-nutrition-1",
            "text": "AAP 2024 Update on Allergenic Food Introduction: Evidence from the LEAP Trial (Du Toit et al., 2015 NEJM, RCT n=640) demonstrates that early introduction of peanuts at 4-6 months for high-risk infants reduces peanut allergy prevalence by 81% (13.7% in avoidance group vs 1.9% in consumption group at 60 months, p<0.001). Current AAP guidance recommends introduction of peanut and egg at 4-6 months, not delayed beyond 6 months, especially for infants with severe eczema or egg allergy. For high-risk infants, consider peanut-specific IgE testing before introduction.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2024, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-rct-leap-1",
            "text": "The Learning Early About Peanut Allergy (LEAP) Trial: A randomized controlled trial of 640 infants aged 4-11 months with severe eczema, egg allergy, or both. Infants were stratified by skin-prick test result and randomized to consume peanut (6g peanut protein/week) or avoid peanut until 60 months. Primary outcome: peanut allergy at 60 months. Results: Among negative skin-prick test stratum, peanut allergy prevalence was 13.7% in avoidance vs 1.9% in consumption group (p<0.001). Among positive skin-prick test stratum: 35.3% vs 10.6% (p=0.004). This landmark RCT fundamentally reversed decades of allergenic food avoidance guidance.",
            "metadata": {"source": "NEJM", "evidence_level": "RCT", "year": 2015, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-aap-vaccine-1",
            "text": "AAP/CDC Recommended Childhood Immunization Schedule (2024): Birth: HepB (dose 1). 2 months: DTaP, Hib, IPV, PCV13, RV, HepB (dose 2). 4 months: DTaP, Hib, IPV, PCV13, RV. 6 months: DTaP, Hib, IPV, PCV13, RV, HepB (dose 3), influenza (annual). 12-15 months: MMR, Varicella, HepA (dose 1), PCV13 booster, Hib booster. 15-18 months: DTaP booster. 4-6 years: DTaP, IPV, MMR, Varicella boosters. 11-12 years: Tdap, HPV (2-dose series), MenACWY. 16 years: MenB (shared clinical decision-making).",
            "metadata": {"source": "AAP/CDC", "evidence_level": "guideline", "year": 2024, "age_stage": "infant", "domain": "vaccination"},
        },
        {
            "id": "seed-who-vaccine-vn-1",
            "text": "Vietnam National Expanded Programme on Immunization (EPI/Tiêm Chủng Mở Rộng) Schedule: Birth: BCG (tuberculosis), HepB (dose 1). 2 months: DPT-VGB-Hib (pentavalent, dose 1), OPV (dose 1). 3 months: DPT-VGB-Hib (dose 2), OPV (dose 2). 4 months: DPT-VGB-Hib (dose 3), OPV (dose 3). 9 months: Measles (dose 1), Measles-Rubella in some provinces. 12 months: Japanese Encephalitis (dose 1). 13 months: Japanese Encephalitis (dose 2). 18 months: DPT booster, Measles-Rubella (dose 2). Additional campaigns may include vitamin A supplementation (6-60 months, twice yearly) and deworming (12-60 months, twice yearly).",
            "metadata": {"source": "Vietnam MOH/WHO", "evidence_level": "guideline", "year": 2024, "age_stage": "infant", "domain": "vaccination"},
        },
    ])

    chunks.extend([
        {
            "id": "seed-sleep-needs-1",
            "text": "National Sleep Foundation Sleep Duration Recommendations (2015, updated 2023): Newborn (0-3 months): 14-17 hours per 24h (acceptable range 11-19h). Infant (4-11 months): 12-15 hours (acceptable 10-18h). Toddler (1-2 years): 11-14 hours (acceptable 9-16h). Preschool (3-5 years): 10-13 hours (acceptable 8-14h). School-age (6-13 years): 9-11 hours (acceptable 7-12h). Adolescent (14-17 years): 8-10 hours (acceptable 7-11h). Young adult (18-25 years): 7-9 hours (acceptable 6-11h). These recommendations are based on a systematic review of 312 scientific articles evaluating sleep duration and health outcomes.",
            "metadata": {"source": "National Sleep Foundation", "evidence_level": "systematic-review", "year": 2015, "age_stage": "all", "domain": "sleep"},
        },
        {
            "id": "seed-adolescent-sleep-1",
            "text": "Adolescent Sleep Phase Delay: Puberty induces a biologically-driven circadian phase delay of approximately 2 hours, shifting the natural sleep onset from ~9pm in childhood to ~11pm in adolescence. Combined with unchanged sleep needs (8-10 hours) and early school start times (often before 8am), this creates chronic sleep deprivation. Consequences include: impaired academic performance, increased motor vehicle accident risk, depression and anxiety, obesity, and increased risk-taking behavior. The American Academy of Pediatrics recommends middle and high schools start no earlier than 8:30am. A 2022 systematic review found that delaying school start times to 8:30am or later increased average sleep duration by 34-45 minutes.",
            "metadata": {"source": "Pediatrics", "evidence_level": "guideline", "year": 2022, "age_stage": "adolescent", "domain": "sleep"},
        },
        {
            "id": "seed-screen-time-1",
            "text": "AAP 2023 Screen Time Guidelines: Under 18 months: Avoid screen media other than video chatting. 18-24 months: Parents who want to introduce digital media should choose high-quality programming and watch it with their children to help them understand what they're seeing. 2-5 years: Limit screen use to 1 hour per day of high-quality programs; co-view with children. 6+ years: Place consistent limits on time spent using media and types of media; ensure media does not displace adequate sleep, physical activity, and other healthy behaviors. Designate media-free times (e.g., dinner, bedroom) and media-free locations (e.g., bedrooms). Content quality and co-engagement matter more than raw time for under-5 children.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "all", "domain": "screen-time"},
        },
        {
            "id": "seed-screen-time-2",
            "text": "Systematic review of 47 studies (2015-2023) on screen time and child development: In children under 2, greater screen time is associated with poorer language development (effect size d=-0.15, p<0.001) and shorter sleep duration (d=-0.20, p<0.01). The association persists after adjusting for socioeconomic status. Content quality moderates the effect: educational content with caregiver interaction shows neutral or positive effects, while passive entertainment content shows negative effects. For children 2-5, >1 hour/day of screen time is associated with higher BMI z-scores and reduced physical activity.",
            "metadata": {"source": "JAMA Pediatrics", "evidence_level": "meta-analysis", "year": 2023, "age_stage": "all", "domain": "screen-time"},
        },
        {
            "id": "seed-language-dev-1",
            "text": "Language Development Milestones (AAP/CDC): By 3 months: coos, recognizes parent voice, startles to loud sounds. 6 months: babbles, responds to name, makes speech-like sounds. 12 months: says 'mama'/'dada' specifically, uses 1-2 words, follows simple commands. 18 months: 10-25 words, points to body parts, follows simple directions. 24 months: 50+ words, 2-word phrases, 50% intelligible to strangers. 36 months: 200+ words, 3-word sentences, 75% intelligible. 48 months: tells stories, 4-5 word sentences, 100% intelligible. Red flags: no babbling by 12 months, no words by 16 months, no 2-word phrases by 24 months, any loss of language skills at any age.",
            "metadata": {"source": "AAP/CDC", "evidence_level": "guideline", "year": 2023, "age_stage": "toddler", "domain": "development"},
        },
        {
            "id": "seed-language-intervention-1",
            "text": "RCT by Suskind et al. (2016, Pediatrics): A parent-directed language intervention (the 3Ts: Tune In, Talk More, Take Turns) randomized 44 low-SES families of children aged 24-36 months. The intervention group received 8 weekly 1-hour home visits with coaching on responsive language strategies. At 6-month follow-up, the intervention group showed significant improvement in parent language input quantity (+2,130 words/day, p<0.01), conversational turn count (+45 turns/day, p<0.05), and child language outcomes measured by CDI vocabulary (+49 words, p<0.01) compared to controls.",
            "metadata": {"source": "Pediatrics", "evidence_level": "RCT", "year": 2016, "age_stage": "toddler", "domain": "development"},
        },
        {
            "id": "seed-tantrum-behavior-1",
            "text": "Evidence-Based Strategies for Toddler Tantrums and Challenging Behavior (AAP, 2023): (1) Maintain consistent routines — predictable schedules reduce anxiety-driven tantrums by providing a sense of control. (2) Offer choices within limits — 'Do you want the red cup or blue cup?' gives autonomy without removing boundaries. (3) Use positive reinforcement — praise specific desired behaviors immediately. (4) Practice planned ignoring for attention-seeking tantrums — ensure safety first, then withdraw attention. (5) Teach emotional vocabulary — label feelings to build emotional regulation. (6) Use time-in rather than time-out — stay with the child during emotional dysregulation and co-regulate. (7) Avoid physical punishment — meta-analytic evidence shows it increases aggression and mental health problems long-term.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "toddler", "domain": "behavior"},
        },
        {
            "id": "seed-attachment-1",
            "text": "Bowlby and Ainsworth's Attachment Theory: Secure attachment develops when caregivers are consistently responsive, sensitive, and available. Key behaviors that promote secure attachment: (1) Responding promptly and warmly to infant cries — does not spoil the child; delayed response is associated with anxious attachment. (2) Physical touch and holding — kangaroo care for preterm infants improves attachment and developmental outcomes. (3) Serve-and-return interactions — the caregiver responds contingently to the child's vocalizations, gestures, and expressions. (4) Emotional availability — being present and attuned during interactions. Secure attachment in infancy predicts better emotional regulation, social competence, academic achievement, and mental health through adolescence and adulthood.",
            "metadata": {"source": "Handbook of Attachment", "evidence_level": "guideline", "year": 2016, "age_stage": "infant", "domain": "emotional-development"},
        },
        {
            "id": "seed-mental-health-adolescent-1",
            "text": "Adolescent Depression Screening (USPSTF Grade B Recommendation, 2022): All adolescents aged 12-18 years should be screened for major depressive disorder (MDD) in primary care settings. The PHQ-A (Patient Health Questionnaire — Adolescents) is a validated 9-item self-report tool for ages 11-17. Scoring: 0-4 = minimal, 5-9 = mild, 10-14 = moderate, 15-19 = moderately severe, 20-27 = severe. Score ≥10 has sensitivity 89% and specificity 77% for MDD. A positive screen must be followed by clinical assessment and referral. Suicide risk assessment (question 9 on PHQ-A) must be immediate — any positive response to suicidality items requires urgent evaluation.",
            "metadata": {"source": "USPSTF/JAMA", "evidence_level": "guideline", "year": 2022, "age_stage": "adolescent", "domain": "mental-health"},
        },
        {
            "id": "seed-mental-health-adolescent-2",
            "text": "Prevalence of Childhood Anxiety Disorders: Merikangas et al. (2010, JAACAP) analyzed the National Comorbidity Survey-Adolescent Supplement (NCS-A), a nationally representative face-to-face survey of 10,123 US adolescents aged 13-18 years. Lifetime prevalence of any anxiety disorder: 31.9%. Specific phobia: 19.3%, social phobia: 9.1%, separation anxiety: 7.6%, PTSD: 5.0%, panic disorder: 2.3%, GAD: 2.2%. Median age of onset for anxiety disorders is 6 years — the earliest of any psychiatric disorder category. 80% of adolescents with anxiety disorders do not receive treatment. Anxiety in childhood predicts adult anxiety, depression, substance use, and educational underachievement.",
            "metadata": {"source": "JAACAP", "evidence_level": "observational", "year": 2010, "age_stage": "adolescent", "domain": "mental-health"},
        },
        {
            "id": "seed-adhd-1",
            "text": "ADHD Diagnosis and Management (AAP Clinical Practice Guideline, 2019): ADHD can be diagnosed in children aged 4-18 years. For preschoolers (4-6 years): first-line treatment is parent training in behavior management (PTBM) and classroom behavioral interventions. Methylphenidate may be considered if behavioral interventions are insufficient. For school-age (6-12 years): FDA-approved medication PLUS behavioral interventions. For adolescents (12-18 years): FDA-approved medication, preferably with behavioral interventions. Diagnostic criteria (DSM-5): ≥6 inattentive and/or hyperactive-impulsive symptoms persisting ≥6 months, onset before age 12, impairment in ≥2 settings, not better explained by another disorder.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2019, "age_stage": "school-age", "domain": "development"},
        },
        {
            "id": "seed-who-growth-1",
            "text": "WHO Child Growth Standards (2006): Based on the WHO Multicentre Growth Reference Study (MGRS) of 8,440 healthy breastfed infants from Brazil, Ghana, India, Norway, Oman, and the USA. The standards describe optimal growth under recommended health behaviors. Key percentiles: 3rd, 15th, 50th, 85th, 97th for weight-for-age, length/height-for-age, weight-for-length/height, BMI-for-age, head circumference-for-age, arm circumference-for-age, subscapular and triceps skinfold-for-age. Underweight defined as weight-for-age < -2 SD (below 3rd percentile). Stunting: height-for-age < -2 SD. Wasting: weight-for-height < -2 SD. Overweight: weight-for-height > +2 SD (ages 0-5) or BMI-for-age > +1 SD (ages 5-19).",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2006, "age_stage": "all", "domain": "growth"},
        },
        {
            "id": "seed-who-growth-2",
            "text": "WHO Child Growth Standards weight-for-age reference values for boys, 50th percentile (kg): Birth: 3.3, 1 month: 4.5, 2m: 5.6, 3m: 6.4, 4m: 7.0, 5m: 7.5, 6m: 7.9, 7m: 8.3, 8m: 8.6, 9m: 8.9, 10m: 9.2, 11m: 9.4, 12m: 9.6, 18m: 10.9, 24m: 12.2, 36m: 14.3, 48m: 16.3, 60m: 18.3. Girls (50th percentile): Birth: 3.2, 1m: 4.2, 2m: 5.1, 3m: 5.8, 4m: 6.4, 5m: 6.9, 6m: 7.3, 7m: 7.6, 8m: 7.9, 9m: 8.2, 10m: 8.5, 11m: 8.7, 12m: 8.9, 18m: 10.2, 24m: 11.5, 36m: 13.9, 48m: 16.1, 60m: 18.2.",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2006, "age_stage": "all", "domain": "growth"},
        },
    ])

    chunks.extend([
        {
            "id": "seed-piaget-1",
            "text": "Piaget's Four Stages of Cognitive Development: (1) Sensorimotor (0-2 years): Infants learn through sensory experience and motor actions. Object permanence develops around 8-12 months — understanding that objects continue to exist when out of sight. (2) Preoperational (2-7 years): Symbolic thinking and language develop rapidly. Thinking is egocentric — children struggle to see things from others' perspectives. Conservation tasks (understanding that quantity remains the same despite changes in appearance) are not yet mastered. (3) Concrete Operational (7-11 years): Logical thinking about concrete events develops. Conservation is understood. Classification and seriation abilities emerge. (4) Formal Operational (12+ years): Abstract reasoning, hypothetical thinking, and systematic problem-solving develop. Not all adults fully achieve formal operational thinking in all domains.",
            "metadata": {"source": "The Psychology of the Child", "evidence_level": "guideline", "year": 1969, "age_stage": "all", "domain": "development-theory"},
        },
        {
            "id": "seed-erikson-1",
            "text": "Erikson's Eight Psychosocial Stages (relevant to childhood): (1) Trust vs. Mistrust (0-18 months): The infant develops a sense of trust when caregivers provide reliable care and affection. A lack of this leads to mistrust. (2) Autonomy vs. Shame/Doubt (18 months-3 years): The child develops a sense of personal control over physical skills and independence. Success leads to autonomy; failure results in shame and doubt. Encourage self-feeding, dressing, and toileting choices. (3) Initiative vs. Guilt (3-5 years): The child asserts power and control through directing play and social interactions. Encourage curiosity and imagination; avoid making the child feel their questions and activities are a nuisance. (4) Industry vs. Inferiority (6-11 years): The child develops competence through school and social activities. Praise effort, not just outcomes. (5) Identity vs. Role Confusion (12-18 years): The adolescent explores different roles and identities. Provide space for exploration while maintaining connection.",
            "metadata": {"source": "Childhood and Society", "evidence_level": "guideline", "year": 1950, "age_stage": "all", "domain": "development-theory"},
        },
        {
            "id": "seed-vygotsky-1",
            "text": "Vygotsky's Zone of Proximal Development (ZPD): The ZPD is the gap between what a child can do independently and what they can achieve with guidance from a more skilled partner (parent, teacher, peer). Effective instruction and parenting should target the ZPD — challenging enough to promote growth but not so difficult that the child experiences repeated failure. Scaffolding is the temporary support provided within the ZPD that is gradually withdrawn as competence increases. Practical applications: (1) Observe what the child can do independently. (2) Provide just enough help for the child to succeed. (3) Gradually reduce support as the child gains mastery. (4) Use questioning rather than direct instruction when possible.",
            "metadata": {"source": "Mind in Society", "evidence_level": "guideline", "year": 1978, "age_stage": "all", "domain": "development-theory"},
        },
        {
            "id": "seed-bronfenbrenner-1",
            "text": "Bronfenbrenner's Ecological Systems Theory: Child development occurs within nested environmental systems. (1) Microsystem: Immediate environment — family, school, peers, neighborhood. The child's direct interactions shape development most powerfully. (2) Mesosystem: Interconnections between microsystems — e.g., parent-teacher communication, family-peer relationships. Strong mesosystem links improve outcomes. (3) Exosystem: Settings that affect the child indirectly — parent's workplace, community resources, mass media. (4) Macrosystem: Cultural values, laws, customs, economic systems. Parenting advice must consider the child's full ecological context, not just individual behaviors. A Vietnamese family's macrosystem differs significantly from a Western family's in terms of filial piety expectations, collectivist values, and educational pressure.",
            "metadata": {"source": "The Ecology of Human Development", "evidence_level": "guideline", "year": 1979, "age_stage": "all", "domain": "development-theory"},
        },
        {
            "id": "seed-motor-milestones-1",
            "text": "WHO Motor Development Milestones Windows (WHO Multicentre Growth Reference Study, 2006): Sitting without support: 3.8-9.2 months (median 5.9m). Standing with assistance: 5.0-11.6 months (median 7.4m). Hands-and-knees crawling: 5.2-13.5 months (median 8.3m). Walking with assistance: 6.0-13.5 months (median 9.0m). Standing alone: 6.9-16.9 months (median 10.8m). Walking alone: 8.2-17.6 months (median 12.0m). Note: These are population-based windows; 4-5% of healthy children will fall outside these windows. Absence of multiple milestones by the upper boundary should trigger developmental evaluation.",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2006, "age_stage": "infant", "domain": "development"},
        },
        {
            "id": "seed-toilet-training-1",
            "text": "Readiness for toilet training typically emerges between 18 and 30 months, with most children achieving daytime continence by 36 months. AAP guidance: Signs of readiness include: (1) Stays dry for 2+ hours. (2) Shows interest in the toilet or potty. (3) Can follow simple instructions. (4) Can communicate the need to go. (5) Dislikes feeling wet or soiled. (6) Can pull pants up and down. Method: Use a child-oriented approach — praise successes, ignore accidents, and never punish. Avoid starting during major life transitions (new sibling, moving, starting daycare). The Brazelton child-oriented approach takes a median of 3-6 months. Nighttime dryness typically develops 6-12 months after daytime control and may not occur until age 5-7.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "toddler", "domain": "development"},
        },
        {
            "id": "seed-nutrition-vitamin-d-1",
            "text": "AAP Vitamin D Supplementation: All breastfed infants and non-breastfed infants consuming <1,000 mL/day of vitamin D-fortified formula should receive 400 IU/day of vitamin D supplementation beginning in the first few days of life and continuing throughout childhood. Vitamin D deficiency causes rickets (impaired bone mineralization) and is associated with increased risk of respiratory infections. Risk factors for deficiency: exclusive breastfeeding without supplementation, dark skin pigmentation, limited sun exposure, maternal vitamin D deficiency during pregnancy.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2024, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-nutrition-iron-1",
            "text": "AAP Iron Supplementation: Breastfed term infants should receive 1 mg/kg/day of oral iron supplementation starting at 4 months of age until iron-rich complementary foods (meat, iron-fortified cereals) are introduced. Preterm infants (<37 weeks) should receive 2 mg/kg/day starting by 1 month through 12 months. Iron deficiency in infancy is associated with long-term cognitive and motor deficits that may persist even after iron status is corrected. Universal screening for iron deficiency anemia is recommended at 12 months (hemoglobin/hematocrit). Formula-fed infants receiving iron-fortified formula do not require additional supplementation.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "infant", "domain": "nutrition"},
        },
        {
            "id": "seed-toilet-training-2",
            "text": "Toilet training methods comparison: A systematic review of 34 studies (2019) compared child-oriented (Brazelton), structured behavioral (Azrin & Foxx), and parent-led approaches. The Azrin & Foxx method (4-6 hour intensive training day) achieves continence fastest (median 4-5 hours) but has higher refusal and relapse rates. The Brazelton child-oriented approach takes longer (median 3-6 months) but shows lower relapse rates and less parent-child conflict. Elimination communication (infant potty training from birth) is practiced in many non-Western cultures including Vietnam, China, and parts of Africa. Key finding: No single method is superior; the best approach is the one that matches the child's temperament, family culture, and parent availability.",
            "metadata": {"source": "Journal of Developmental & Behavioral Pediatrics", "evidence_level": "systematic-review", "year": 2019, "age_stage": "toddler", "domain": "development"},
        },
        {
            "id": "seed-tantrum-physiology-1",
            "text": "The neurobiology of toddler tantrums: The prefrontal cortex (PFC), responsible for emotional regulation, impulse control, and rational decision-making, is not fully developed until approximately age 25. The amygdala (emotional center) is fully functional from birth. When a toddler experiences frustration, the amygdala triggers a fight-or-flight response that the immature PFC cannot inhibit. The result is a tantrum — not manipulation, but a neurobiologically normal overflow of emotion. Effective response: (1) Ensure safety. (2) Stay calm — your regulated nervous system co-regulates theirs. (3) Validate feelings without validating destructive behavior. (4) Wait for the storm to pass before problem-solving — the learning brain is offline during peak emotional arousal.",
            "metadata": {"source": "The Whole-Brain Child (Siegel & Bryson)", "evidence_level": "guideline", "year": 2011, "age_stage": "toddler", "domain": "behavior"},
        },
        {
            "id": "seed-sibling-rivalry-1",
            "text": "Managing sibling rivalry and preparing for a new baby (AAP): (1) Tell the older child about the pregnancy when you start telling others — use concrete language. (2) Involve the older sibling in preparations — choosing clothes, setting up the nursery. (3) Maintain the older child's routines as much as possible after the baby arrives. (4) Give the older child special one-on-one time daily (even 10-15 minutes). (5) Do not blame the baby for limitations ('I can't play right now, the baby is nursing' vs 'Let's have special time in 15 minutes'). (6) Expect regression — temporary loss of toileting or language skills is common and normal. Respond with patience, not punishment. (7) Allow expression of negative feelings toward the baby — acknowledge and validate rather than suppress.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "toddler", "domain": "behavior"},
        },
        {
            "id": "seed-bullying-1",
            "text": "Evidence-based bullying prevention and response (APA, 2022): Bullying affects 20-30% of school-age children. Signs a child may be bullied: unexplained injuries, lost/destroyed belongings, frequent headaches/stomachaches, changes in eating/sleeping, declining grades, avoidance of school/social situations, self-destructive behaviors. Parent response: (1) Listen calmly without overreacting. (2) Document specific incidents. (3) Contact the school — work collaboratively with teacher, counselor, and principal. (4) Do NOT contact the bully's parents directly — this often escalates. (5) Teach assertive responses (not aggressive): 'Stop, I don't like that' delivered with confident posture. (6) Build resilience through extracurricular activities that build competence and friendships outside the bullying context. (7) If cyberbullying: save evidence, block the perpetrator, report to platform.",
            "metadata": {"source": "APA", "evidence_level": "guideline", "year": 2022, "age_stage": "school-age", "domain": "behavior"},
        },
        {
            "id": "seed-puberty-1",
            "text": "Normal Puberty Timeline: Girls — breast development (thelarche): 8-13 years (mean 10 years). Pubic hair (pubarche): 8-14 years. Peak height velocity: 11.4-12.2 years (mean 11.7). Menarche (first period): 10-16 years (mean 12.4 years in US; 12.9 years globally). The sequence is: thelarche → pubarche → peak growth → menarche. Boys — testicular enlargement: 9-14 years (mean 11.5). Pubic hair: 10-15 years. Peak height velocity: 13-14 years (mean 13.5). Voice deepening, facial hair follow. Precocious puberty: breast development <8 years in girls, testicular enlargement <9 years in boys — warrants endocrine evaluation. Delayed puberty: no breast development by 13 in girls, no testicular enlargement by 14 in boys.",
            "metadata": {"source": "AAP/Endocrine Society", "evidence_level": "guideline", "year": 2023, "age_stage": "adolescent", "domain": "development"},
        },
        {
            "id": "seed-teen-communication-1",
            "text": "Evidence-based strategies for parent-adolescent communication (APA, 2023): (1) Listen more than you talk — aim for a 70:30 ratio in conversations. (2) Ask open-ended questions ('What was the best part of your day?' vs 'Did you have a good day?'). (3) Avoid interrogation — parallel activities (driving, walking, cooking together) facilitate conversation better than face-to-face questioning. (4) Validate feelings before problem-solving — 'That sounds really hard' before 'Here's what you should do.' (5) Share your own adolescent experiences appropriately — this normalizes struggles. (6) Respect privacy while maintaining safety monitoring. (7) Pick battles — hair color is not worth a relationship rupture; substance use is. (8) Maintain family rituals (dinner, movie night) even as the adolescent resists — consistent connection is protective.",
            "metadata": {"source": "APA", "evidence_level": "guideline", "year": 2023, "age_stage": "adolescent", "domain": "emotional-development"},
        },
        {
            "id": "seed-divorce-transition-1",
            "text": "Supporting children through parental separation and divorce (AACAP, 2023): Children's reactions vary by developmental stage. Preschoolers (2-5): May blame themselves, show regression, separation anxiety. Reassure concretely that both parents love them and the divorce is not their fault. School-age (6-11): May fantasize about reconciliation, feel divided loyalty, express anger. Maintain consistent routines across both homes. Adolescents (12-18): May question relationships and authority, take on premature adult roles or act out. Keep them out of the middle — never use them as messengers or confidants about the other parent. Universal recommendations: (1) Minimize conflict in front of children — conflict exposure, not divorce itself, predicts poor outcomes. (2) Maintain consistent discipline between homes. (3) Support the child's relationship with both parents (unless safety concerns). (4) Seek professional help if child shows persistent sadness, academic decline, or behavioral changes.",
            "metadata": {"source": "AACAP", "evidence_level": "guideline", "year": 2023, "age_stage": "all", "domain": "emotional-development"},
        },
    ])

    chunks.extend([
        {
            "id": "seed-obesity-prevention-1",
            "text": "AAP Clinical Practice Guideline for the Evaluation and Treatment of Children and Adolescents With Obesity (2023): Childhood obesity affects 14.7 million US children (19.7% prevalence). The guideline recommends: (1) Comprehensive evaluation including medical history, physical examination, laboratory screening for comorbidities. (2) Intensive health behavior and lifestyle treatment (IHBLT) — ≥26 contact hours over 3-12 months with family-based multicomponent intervention. (3) For children 6-11 years with severe obesity, weight-loss pharmacotherapy (liraglutide, semaglutide) may be considered alongside IHBLT. (4) For adolescents ≥13 years with severe obesity (BMI ≥120% of 95th percentile), metabolic and bariatric surgery may be considered. (5) Watchful waiting or delayed treatment is no longer recommended — obesity should be treated early and intensively.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "all", "domain": "nutrition"},
        },
        {
            "id": "seed-childcare-selection-1",
            "text": "Selecting quality child care (AAP, 2023): Key quality indicators: (1) Low child-to-caregiver ratios — infants <1:4, toddlers 1:4-6, preschoolers 1:8-10. (2) Small group sizes. (3) Caregiver qualifications — training in child development or early childhood education. (4) Low staff turnover — continuity of caregiving relationships matters. (5) Safe physical environment — age-appropriate equipment, safe sleep practices for infants, fenced outdoor play area. (6) Positive caregiver-child interactions — warm, responsive, language-rich. The NICHD Study of Early Child Care found that higher-quality child care is associated with better cognitive and language outcomes through elementary school, while quantity of care (>30 hours/week) is associated with slightly increased behavioral problems, moderated by care quality and family factors.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "infant", "domain": "general-pediatrics"},
        },
        {
            "id": "seed-reading-aloud-1",
            "text": "The American Academy of Pediatrics recommends that pediatricians promote reading aloud from birth during well-child visits (the 'Reach Out and Read' model). Reading aloud daily to infants and young children: (1) Increases vocabulary at 24 months by approximately 20,000 words per year for children read to daily vs. rarely. (2) Activates brain networks supporting narrative comprehension and visual imagery in fMRI studies. (3) Strengthens parent-child bonding and secure attachment. (4) Provides a protective factor for children from low-SES backgrounds against the word gap (30 million word gap by age 3; Hart & Risley, 1995). For infants under 6 months, choose high-contrast board books. For 6-12 months, books with textures, flaps, and simple images. By 18-24 months, children can identify familiar objects and anticipate story events.",
            "metadata": {"source": "AAP/Pediatrics", "evidence_level": "guideline", "year": 2023, "age_stage": "infant", "domain": "development"},
        },
        {
            "id": "seed-fever-management-1",
            "text": "Fever Management in Children (AAP, 2023): Fever is defined as rectal temperature ≥38°C (100.4°F). Fever itself is not harmful — it is a physiological defense mechanism. Treat the child's comfort, not the thermometer reading. When to treat: if the child is uncomfortable, in pain, or irritable — not solely based on the temperature number. Medication: Acetaminophen (paracetamol) 10-15 mg/kg every 4-6 hours, maximum 5 doses in 24 hours. Ibuprofen 5-10 mg/kg every 6-8 hours (only for children ≥6 months). Do NOT alternate acetaminophen and ibuprofen routinely — this increases dosing error risk. Do NOT use aspirin (Reye syndrome risk). Red flags requiring immediate medical evaluation: fever in infant ≤3 months (rectal ≥38°C), fever >40.5°C (105°F), fever persisting >72 hours, fever with lethargy/irritability/neck stiffness/seizure/difficulty breathing/purple rash/dehydration.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "all", "domain": "general-pediatrics"},
        },
        {
            "id": "seed-maternal-mental-health-1",
            "text": "Maternal Perinatal Mental Health (ACOG, 2023): Perinatal mood and anxiety disorders (PMADs) affect 1 in 7 women during pregnancy or the first year postpartum. The term 'PMAD' encompasses: postpartum depression (PPD), postpartum anxiety, postpartum OCD, postpartum PTSD, and postpartum psychosis. PPD: onset within 4 weeks after delivery, symptoms include persistent sadness, anhedonia, guilt, sleep disturbance (beyond expected), difficulty bonding with baby. Screening: Edinburgh Postnatal Depression Scale (EPDS) — score ≥10 suggests possible depression; score ≥13 indicates high probability. Any positive response to question 10 (self-harm thoughts) requires emergency evaluation. Paternal depression also occurs — 10% of fathers experience depression in the first year postpartum, with negative effects on child behavioral outcomes.",
            "metadata": {"source": "ACOG", "evidence_level": "guideline", "year": 2023, "age_stage": "newborn", "domain": "mental-health"},
        },
        {
            "id": "seed-play-development-1",
            "text": "The AAP's 2018 clinical report 'The Power of Play' emphasizes that play is essential for healthy brain development. Play types by age: Sensorimotor play (0-2 years): exploring objects through senses and motor actions — mouthing, shaking, banging, dropping. Symbolic/pretend play (2-7 years): using objects to represent other things — a block becomes a phone. Emerges around 18-24 months. Cooperative play (4+ years): playing with peers toward shared goals with rules. The report cites evidence that play: (1) Builds executive function — self-regulation, working memory, cognitive flexibility. (2) Reduces toxic stress by providing joyful, nurturing interactions that buffer cortisol. (3) Supports language development through peer and adult interaction. (4) Promotes physical health and motor development. The AAP recommends pediatricians write a 'prescription for play' at every well-child visit.",
            "metadata": {"source": "AAP/Pediatrics", "evidence_level": "guideline", "year": 2018, "age_stage": "all", "domain": "development"},
        },
        {
            "id": "seed-llm-pediatrics-1",
            "text": "Scoping review of large language models in pediatric clinical decision support (Chen et al., 2024, npj Digital Medicine): Review of 47 studies evaluating LLM performance on pediatric tasks. Findings: (1) LLMs demonstrate 76-92% accuracy on board-style pediatric multiple-choice questions. (2) Performance degrades significantly on nuanced clinical scenarios requiring integration of developmental context, family preferences, and social determinants. (3) Hallucination rate is 8-18% for pediatric factual recall. (4) RAG-augmented LLMs reduce hallucination to 3-7% for pediatric knowledge questions when backed by curated guidelines. (5) All current LLMs show age-agnostic tendencies — they fail to calibrate advice to developmental stage without explicit age-stage prompting. Key safety recommendation: LLMs should not be used unsupervised for pediatric clinical decisions; they are most effective as information retrieval and summarization tools with human oversight.",
            "metadata": {"source": "npj Digital Medicine", "evidence_level": "systematic-review", "year": 2024, "age_stage": "all", "domain": "ai-safety"},
        },
        {
            "id": "seed-rag-medical-1",
            "text": "RAG for Medical Question Answering: Benchmarks and Challenges (Zhang et al., 2024, ArXiv): Evaluated RAG architectures on medical Q&A benchmarks including MedQA, PubMedQA, and MMLU-Med. Key findings: (1) RAG with curated medical knowledge sources outperforms closed-book LLM on factual accuracy by 23-41% across benchmarks. (2) Retrieval quality dominates — increasing top-K from 3 to 8 improves answer completeness but degrades precision when K > 10 due to noise. (3) Hybrid retrieval (dense + sparse) outperforms either alone for medical text. (4) Evidence-level filtering (prioritizing RCTs and guidelines over case reports) improves answer quality by 15% as rated by physician evaluators. (5) Best practice: retrieve 8-12 chunks, re-rank by evidence quality and recency, and present top 5 as context with evidence-level badges.",
            "metadata": {"source": "ArXiv", "evidence_level": "meta-analysis", "year": 2024, "age_stage": "all", "domain": "ai-safety"},
        },
    ])

    chunks.extend([
        {
            "id": "seed-discipline-positive-1",
            "text": "AAP Policy Statement on Effective Discipline (2018): The AAP strongly recommends against the use of physical punishment, including spanking. Evidence shows: (1) Spanking is associated with increased aggression, antisocial behavior, and mental health problems in longitudinal studies. (2) Spanking does not improve long-term compliance or behavior. (3) The negative outcomes of spanking are consistent across cultures and study designs. Recommended alternatives: (1) Positive reinforcement of desired behaviors. (2) Natural and logical consequences. (3) Time-out from positive reinforcement (1 minute per year of age, max 5 minutes). (4) Parental attention withdrawal for minor misbehavior. (5) Clear, consistent, age-appropriate rules. (6) Modeling desired emotional regulation. Critical: Time-out is for brief removal from reinforcement, not isolation or humiliation.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2018, "age_stage": "all", "domain": "behavior"},
        },
        {
            "id": "seed-picky-eating-1",
            "text": "Evidence-based management of picky eating (AAP, 2023): Picky eating is developmentally normal — peaks between 2-6 years and resolves in most children. The 'Division of Responsibility' (Satter model): Parent is responsible for WHAT food is served, WHEN, and WHERE. Child is responsible for HOW MUCH to eat and WHETHER to eat. Key strategies: (1) Offer new foods alongside accepted foods — repeated neutral exposure (8-15 exposures) increases acceptance. (2) Do not pressure, bribe, or force — this backfires and creates negative associations. (3) Avoid short-order cooking — serve one family meal. (4) Eat together — parental modeling of eating the target food increases child acceptance. (5) Keep meals to 20-30 minutes. (6) Avoid grazing between planned meals and snacks — mild hunger drives food exploration. Red flags for feeding disorder: weight loss/failure to thrive, <20 accepted foods, gagging/vomiting with new foods, extreme food selectivity by texture.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "toddler", "domain": "nutrition"},
        },
        {
            "id": "seed-executive-function-1",
            "text": "Executive Function Development: Executive functions (EF) are the brain's 'air traffic control system' — working memory, inhibitory control, and cognitive flexibility. EF develops rapidly from 3-5 years with another spurt in adolescence (myelination of prefrontal cortex). Activities that build EF in young children: (1) Pretend play — requires holding roles in mind, inhibiting reality, and flexibly adapting scenarios. (2) Storytelling and narrative — recalling sequence, imagining alternatives. (3) Songs with gestures (e.g., Head, Shoulders, Knees, and Toes) — working memory + inhibitory control. (4) Simple board games — turn-taking, rule-following, strategy. (5) Simon Says — pure inhibitory control practice. (6) Free play with peers — negotiating roles and rules builds all three EF components. For school-age children: martial arts, music training, mindfulness, and aerobic exercise all show EF benefits in controlled studies.",
            "metadata": {"source": "Center on the Developing Child (Harvard)", "evidence_level": "guideline", "year": 2020, "age_stage": "all", "domain": "development"},
        },
        {
            "id": "seed-substance-abuse-teen-1",
            "text": "Adolescent Substance Use Prevention (AAP, 2023): The adolescent brain is uniquely vulnerable to substance effects and addiction due to ongoing prefrontal cortex development and heightened dopamine sensitivity in the reward system. Key prevention strategies: (1) Start conversations early (age 9-10) about tobacco, alcohol, and drugs. (2) Use 'teachable moments' from media, news, or community events. (3) Set clear family expectations — 'In our family, we wait until 21 to drink alcohol' is more effective than 'Don't drink.' (4) Monitor without hovering — know friends, whereabouts, and online activity. (5) Model healthy coping — parental substance use is a strong predictor of adolescent use. (6) Discuss peer pressure and rehearse refusal skills. Warning signs: declining grades, change in friend group, secretive behavior, missing items/money, mood swings beyond normal adolescence, bloodshot eyes, changes in sleep/eating.",
            "metadata": {"source": "AAP", "evidence_level": "guideline", "year": 2023, "age_stage": "adolescent", "domain": "mental-health"},
        },
        {
            "id": "seed-academic-pressure-vn-1",
            "text": "Academic Pressure and Child Mental Health in East Asian Contexts: A systematic review of 38 studies (2020) examining academic stress in East Asian educational systems including Vietnam, China, South Korea, Japan, and Singapore. Findings: Academic pressure is positively correlated with anxiety (r=0.34, p<0.001), depression (r=0.29, p<0.001), and sleep disturbance (r=0.26, p<0.01) in adolescents. Vietnamese students face unique pressures from the national high school entrance exam (thi vào lớp 10) and university entrance exam (thi THPT Quốc gia). Parental expectations that focus on effort ('I'm proud of how hard you worked') rather than outcome ('Why didn't you get an A?') are associated with lower anxiety and higher academic self-efficacy. Recommended: balance academic expectations with unstructured time, physical activity, adequate sleep, and family connection.",
            "metadata": {"source": "Asian Journal of Psychiatry", "evidence_level": "systematic-review", "year": 2020, "age_stage": "adolescent", "domain": "mental-health"},
        },
        {
            "id": "seed-physical-activity-1",
            "text": "Physical Activity Guidelines for Children and Adolescents (WHO, 2020): Children and adolescents aged 5-17 years should do at least 60 minutes per day of moderate-to-vigorous physical activity (MVPA). At least 3 days per week should include vigorous-intensity aerobic activities and activities that strengthen muscle and bone. For children under 5: Infants (<1 year): be physically active several times a day — at least 30 minutes of tummy time spread throughout the day when awake. Toddlers (1-2 years): at least 180 minutes of any intensity physical activity spread throughout the day. Preschoolers (3-4 years): at least 180 minutes including at least 60 minutes of MVPA. Sedentary screen time is not recommended for children under 2, and should be limited to <1 hour/day for ages 2-4; less is better.",
            "metadata": {"source": "WHO", "evidence_level": "guideline", "year": 2020, "age_stage": "all", "domain": "general-pediatrics"},
        },
    ])

    return chunks


def seed_knowledge_base(force: bool = False) -> dict:
    ks = get_knowledge_store()
    embed_svc = get_embedding_service()

    existing_count = ks.count()
    if existing_count > 0 and not force:
        logger.info("Knowledge base already has %d chunks. Use force=True to re-seed.", existing_count)
        return {"status": "skipped", "existing_count": existing_count}

    chunks = _generate_seed_chunks()
    logger.info("Generating embeddings for %d seed chunks...", len(chunks))

    embedded_chunks: list[dict] = []
    for chunk in chunks:
        embedding = embed_svc.embed([chunk["text"]])[0]
        embedded_chunks.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "embedding": embedding,
        })

    ks.upsert_chunks(embedded_chunks)
    logger.info("Seeded knowledge base with %d chunks.", len(embedded_chunks))

    if SEED_DATA_PATH.parent.exists():
        seed_data = {
            "seeded_at": datetime.now(timezone.utc).isoformat(),
            "chunk_count": len(chunks),
            "chunks": chunks,
        }
        SEED_DATA_PATH.write_text(json.dumps(seed_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"status": "success", "chunks_seeded": len(embedded_chunks)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, force=True)
    seed_knowledge_base()
