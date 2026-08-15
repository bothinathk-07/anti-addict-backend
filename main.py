from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Anti-Addict Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AssessmentPayload(BaseModel):
    user_id: str = Field(min_length=1)
    score: int = Field(ge=0, le=100)


class PredictionPayload(BaseModel):
    features: list[float] = Field(min_length=1, max_length=20)


@app.get("/health")
def health():
    return {"status": "ok", "service": "anti-addict-backend"}


@app.post("/assessment/submit")
def submit_assessment(payload: AssessmentPayload):
    return {"message": "assessment received", "user_id": payload.user_id, "score": payload.score}


@app.post("/predict")
def predict(payload: PredictionPayload):
    if not payload.features:
        raise HTTPException(status_code=400, detail="features must not be empty")

    raw_score = sum(payload.features) * 10
    score = int(min(100, max(0, raw_score)))
    return {
        "riskLevel": "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW",
        "riskScore": score,
        "confidence": 0.9,
    }
