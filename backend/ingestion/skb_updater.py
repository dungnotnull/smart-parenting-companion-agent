import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SKB_PATH = Path(__file__).resolve().parent.parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"


def _read_skb() -> str:
    if SKB_PATH.exists():
        return SKB_PATH.read_text(encoding="utf-8")
    return ""


def _write_skb(content: str):
    SKB_PATH.write_text(content, encoding="utf-8")


def append_update_log(
    source: str,
    papers_added: int,
    topics: list[str],
    notable_findings: str,
):
    content = _read_skb()

    marker = "## Knowledge Update Log"
    marker_idx = content.find(marker)
    if marker_idx == -1:
        logger.warning("SKB.md missing Knowledge Update Log section")
        return

    insert_idx = content.find("\n### ", marker_idx)
    if insert_idx == -1:
        insert_idx = content.find("\n---", marker_idx)
    if insert_idx == -1:
        insert_idx = len(content)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    topic_list = ", ".join(topics[:8]) if topics else "various domains"
    log_entry = (
        f"\n\n### {today}\n"
        f"- Source: {source}\n"
        f"- Papers added: {papers_added}\n"
        f"- Topics covered: {topic_list}\n"
        f"- Notable findings: {notable_findings[:200]}\n"
    )

    new_content = content[:insert_idx] + log_entry + content[insert_idx:]
    _write_skb(new_content)
    logger.info("SKB.md updated with %d papers from %s", papers_added, today)


def update_research_papers_table(title: str, authors: str, year: str, venue: str, doi_or_url: str, relevance: str):
    content = _read_skb()

    marker = "## Key Research Papers"
    marker_idx = content.find(marker)
    if marker_idx == -1:
        logger.warning("SKB.md missing Key Research Papers section")
        return

    insert_idx = content.find("\n### ", marker_idx)
    if insert_idx == -1:
        insert_idx = content.find("\n## ", marker_idx + 1)
    if insert_idx == -1:
        insert_idx = len(content)

    new_entry = (
        f"| {title} | {authors} | {year} | {venue} | {doi_or_url} | {relevance} |\n"
    )

    new_content = content[:insert_idx] + new_entry + content[insert_idx:]
    _write_skb(new_content)
    logger.info("SKB.md research papers table updated with: %s", title)


def get_last_update_date() -> Optional[str]:
    content = _read_skb()
    marker = "## Knowledge Update Log"
    marker_idx = content.find(marker)
    if marker_idx == -1:
        return None

    date_section_start = content.find("### ", marker_idx)
    if date_section_start == -1:
        return None

    date_section_end = content.find("\n", date_section_start + 4)
    if date_section_end == -1:
        date_section_end = date_section_start + 14

    date_str = content[date_section_start + 4:date_section_end].strip()
    return date_str if date_str else None
