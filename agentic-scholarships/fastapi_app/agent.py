from typing import Any, Dict, List
import os
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from .scholarship_data import SCHOLARSHIPS

@tool("list_scholarships", return_direct=False)
def list_scholarships() -> List[Dict[str, Any]]:
    """Return the full list of scholarships."""
    return SCHOLARSHIPS

@tool("filter_scholarships", return_direct=True)
def filter_scholarships(query: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filter scholarships based on a query dict with fields: track, tenth, inter, btech, income, category, state."""
    track = (query.get("track") or "").lower()
    tenth = float(query.get("tenth", 0))
    inter = float(query.get("inter", 0))
    btech = float(query.get("btech", 0))
    income = float(query.get("income", 999999999))
    category = (query.get("category") or "GEN").upper()
    state = (query.get("state") or "ALL").upper()

    results = []
    for s in SCHOLARSHIPS:
        if s["track"] != track:
            continue
        if tenth < s["min_10_cgpa"]:
            continue
        if track == "engineering" and inter < s["min_inter_cgpa"]:
            continue
        # Only enforce B.Tech CGPA if user provided a non-zero value
        if track == "engineering" and btech > 0 and btech < s["min_btech_cgpa"]:
            continue
        # Ignore family income filter to show scholarships for all income levels
        if category not in s["category"]:
            continue
        if "ALL" not in s["states"] and state not in s["states"]:
            continue
        results.append(s)
    return results

# A simple agent-ish pipeline using LangChain Runnables and Tools (no external LLM needed)
def build_agent_pipeline():
    def _evaluate(query: Dict[str, Any], s: Dict[str, Any]):
        reasons: List[str] = []
        eligible = True
        if s["track"] != query["track"]:
            eligible = False; reasons.append(f"Track mismatch: needs {s['track']}")
        if query["tenth"] < s["min_10_cgpa"]:
            eligible = False; reasons.append(f"10th CGPA < {s['min_10_cgpa']}")
        if query["track"] == "engineering" and query["inter"] < s["min_inter_cgpa"]:
            eligible = False; reasons.append(f"Inter CGPA < {s['min_inter_cgpa']}")
        # Only enforce B.Tech CGPA if user provided a non-zero value
        if query["track"] == "engineering" and query["btech"] > 0 and query["btech"] < s["min_btech_cgpa"]:
            eligible = False; reasons.append(f"B.Tech CGPA < {s['min_btech_cgpa']}")
        # Income ignored per user requirement to show all income levels
        if query["category"] not in s["category"]:
            eligible = False; reasons.append("Category not eligible")
        state = query["state"]
        if "ALL" not in s["states"] and state not in s["states"]:
            eligible = False; reasons.append(f"State not in {s['states']}")
        enriched = dict(s)
        enriched.update({"eligible": eligible, "reasons": reasons})
        return enriched

    def _run(query: Dict[str, Any]):
        # Return all scholarships with eligibility flags and reasons
        return [_evaluate(query, s) for s in SCHOLARSHIPS]
    return RunnableLambda(_run)
