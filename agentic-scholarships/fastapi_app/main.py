from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import jwt

from shared.config import ALLOWED_ORIGINS, JWT_SECRET, OPENAI_API_KEY
from .agent import build_agent_pipeline
from openai import OpenAI

app = FastAPI(title="Scholarship Opportunities API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    track: str = Field(description="engineering or intermediate")
    tenth_cgpa: float
    inter_cgpa: float
    btech_cgpa: Optional[float] = 0.0
    family_income: int
    category: str
    state: str
    use_llm: bool = False

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/recommend"):
        # Allow CORS preflight without auth
        if request.method == "OPTIONS":
            return await call_next(request)
        # Dev bypass: allow unauthenticated access so UI always works during development
        pass
    return await call_next(request)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    agent = build_agent_pipeline()
    # Basic log (stdout) for debugging payloads
    print({
        "track": req.track,
        "tenth": req.tenth_cgpa,
        "inter": req.inter_cgpa,
        "btech": req.btech_cgpa,
        "income": req.family_income,
        "category": req.category,
        "state": req.state,
        "use_llm": req.use_llm,
    })
    query = {
        "track": req.track.lower(),
        "tenth": req.tenth_cgpa,
        "inter": req.inter_cgpa,
        "btech": req.btech_cgpa or 0.0,
        "income": req.family_income,
        "category": (req.category).upper(),
        "state": (req.state).upper(),
    }
    results: List[Dict[str, Any]] = agent.invoke(query)

    llm_summary = None
    if req.use_llm and OPENAI_API_KEY:
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            eligible = [r for r in results if r.get("eligible")]
            prompt = (
                "Summarize the top scholarship matches for a student. "
                "For each, provide a one-line reason. If none eligible, advise the closest fit. "
                f"Data: {eligible[:5]}"
            )
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=200,
            )
            llm_summary = completion.choices[0].message.content
        except Exception as e:
            llm_summary = None

    return {"matches": results, "llm_summary": llm_summary}
