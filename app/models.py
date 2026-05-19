from pydantic import BaseModel
from typing import List, Optional

class PromptRequest(BaseModel):
    prompt: str

class AnalysisResult(BaseModel):
    prompt: str
    score: int
    risk_level: str
    triggered_rules: List[str]
    decision: str
    message: str
    ia_response: Optional[str] = None
