import re
from typing import Optional


class EntityExtractor:
    def __init__(self, model_name: str = "dslim/bert-base-NER"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "ner",
                    model=self.model_name,
                    aggregation_strategy="simple",
                )
            except Exception:
                self._pipeline = False
        return self._pipeline if self._pipeline is not False else None

    def extract(self, text: str) -> dict:
        pipe = self.pipeline
        if pipe is not None:
            try:
                entities = pipe(text[:1024])
                return self._structure_entities(entities)
            except Exception:
                pass
        return self._regex_fallback(text)

    def _structure_entities(self, raw_entities: list[dict]) -> dict:
        age_ranges: list[str] = []
        conditions: list[str] = []
        interventions: list[str] = []
        organizations: list[str] = []

        for ent in raw_entities:
            label = ent.get("entity_group", ent.get("entity", ""))
            word = ent.get("word", "")
            if "ORG" in label:
                organizations.append(word)
            elif "PER" in label:
                pass
            else:
                conditions.append(word)

        text_lower = " ".join([e.get("word", "") for e in raw_entities]).lower()
        age_ranges = self._extract_age_patterns(text_lower)

        return {
            "age_ranges": age_ranges,
            "conditions": list(set(conditions))[:10],
            "interventions": list(set(interventions))[:10],
            "organizations": list(set(organizations))[:5],
        }

    def _regex_fallback(self, text: str) -> dict:
        text_lower = text.lower()

        age_ranges = self._extract_age_patterns(text_lower)

        conditions = list(set(re.findall(
            r'\b(?:anxiety|depression|asthma|obesity|adhd|autism|'
            r'eczema|allergy|diabetes|autism spectrum|developmental delay|'
            r'sids|colic|reflux|jaundice|anemia|rickets)\b', text_lower
        )))

        interventions = list(set(re.findall(
            r'\b(?:breastfeeding|vaccination|vitamin\s*d\s*supplementation|'
            r'iron\s*supplementation|tummy\s*time|sleep\s*training|'
            r'cognitive\s*behavioral\s*therapy|parent\s*training)\b', text_lower
        )))

        organizations = list(set(re.findall(
            r'\b(?:AAP|WHO|CDC|USPSTF|NICHD|UNICEF)\b', text
        )))

        return {
            "age_ranges": age_ranges,
            "conditions": conditions,
            "interventions": interventions,
            "organizations": organizations,
        }

    @staticmethod
    def _extract_age_patterns(text: str) -> list[str]:
        patterns = [
            r'(\d+[-–]\d+\s*(?:months?|years?|m|y)\s*(?:old)?)',
            r'(?:under|less than|below)\s*(\d+\s*(?:months?|years?))',
            r'(?:over|older than|above)\s*(\d+\s*(?:months?|years?))',
            r'(\d+\s*(?:months?|years?)\s*(?:of age|old))',
            r'(?:infants?|newborns?|toddlers?|preschoolers?|adolescents?)',
        ]
        matches: list[str] = []
        for pattern in patterns:
            found = re.findall(pattern, text)
            if isinstance(found[0], tuple) if found else False:
                matches.extend([str(f) for f in found if f])
            else:
                matches.extend(found)
        return list(set(matches))[:10]


_entity_extractor_instance: Optional[EntityExtractor] = None


def get_entity_extractor() -> EntityExtractor:
    global _entity_extractor_instance
    if _entity_extractor_instance is None:
        _entity_extractor_instance = EntityExtractor()
    return _entity_extractor_instance
