from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph

app = FastAPI()

class ArticleInput(BaseModel):
    article_text: str
    headline: str = "" # Optional, will be extracted if empty or ignored

@app.post("/analyze")
def analyze_article(data: ArticleInput):
    state = {
        "article_text": data.article_text,
        "headline": data.headline
    }
    result = graph.invoke(state)
    
    # Strict Output Format
    return {
        "headline": result.get("headline", ""),
        "verdict": result.get("verdict", "UNCERTAIN"),
        "confidence": result.get("confidence", "50%"),
        "summary": result.get("summary", ""),
        "alternatives": result.get("alternatives", [])
    }
