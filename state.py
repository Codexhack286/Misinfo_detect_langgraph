from typing import TypedDict, Optional, List, Dict

class MisinformationState(TypedDict):
    headline: str
    article_text: str

    search_results: Optional[List[str]]
    fact_check_result: Optional[Dict]

    verdict: Optional[str]      # "SAFE TO PROCEED" | "POTENTIAL MISINFORMATION" | "UNCERTAIN"
    confidence: Optional[str]   # "XX%"

    summary: Optional[str]
    alternatives: Optional[List[Dict]] # alternatives tool returns list of dicts
