# 🕵️‍♂️ Misinformation Verification Agent

A robust, multi-layered AI agent designed to verify news headlines and claims using a combination of Google FactCheck, DuckDuckGo Search, and Perplexity AI (for post-2024 active search).

## 🌟 Key Features

*   **Multi-Step Verification**: Uses a directed cyclic graph (LangGraph) to orchestrate verification.
*   **Headline Extraction**: Automatically extracts the core claim/headline from long articles using an LLM.
*   **Strict Fact-Checking**: Prioritizes authoritative sources from the Google FactCheck Tools API.
*   **Real-Time Fallback**: Smart fallback to **Perplexity AI** for recent events (post-2024) or claims not yet indexed by traditional fact-checkers.
*   **Trusted Alternatives**: Fetches reliable news sources if a claim is debunked.
*   **Streamlit Frontend**: Clean, interactive UI for easy testing and demonstrations.

## 🏗️ Architecture

The agent follows a **LangGraph** workflow:

1.  **Extract**: Pulls the exact headline from input text.
2.  **Search**: Verifies the presence of the claim across the web.
3.  **Fact Check**: Queries Google's Fact Check Validator.
    *   *If definitive:* Returns `SAFE` or `MISINFORMATION`.
    *   *If uncertain:* Triggers Fallback.
4.  **Perplexity Fallback**: Uses LLM-driven live search to determine if the claim is "obviously true" or "obviously false" based on the latest web data.
5.  **Route**: Finalizes the verdict and generates a summary/alternatives.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   API Keys for:
    *   **Groq** (LLM)
    *   **Google FactCheck Tools**
    *   **NewsAPI** (for alternatives)
    *   **Perplexity AI** (for fallback)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/DTL.git
    cd DTL
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY="your_groq_key"
    GOOGLE_FACTCHECK_KEY="your_google_key"
    NEWS_API_KEY="your_newsapi_key"
    PERPLEXITY_API_KEY="your_perplexity_key"
    ```

### 🏃‍♂️ Running the Application

**Option 1: Streamlit Frontend (Recommended)**
Use the interactive web UI:
```bash
streamlit run frontend.py
```

**Option 2: Backend API**
Run the FastAPI server:
```bash
uvicorn app:app --reload
```

**Option 3: Trace a Workflow**
See the agent's "thought process" in the terminal:
```bash
python trace_workflow.py "The moon is made of green cheese"
```

## 🧪 Output Format

The agent provides a strict JSON output:

```json
{
  "headline": "Extracted Claim",
  "verdict": "SAFE TO PROCEED | POTENTIAL MISINFORMATION | UNCERTAIN",
  "confidence": "95%",
  "summary": "Explanation of why the claim is true or false...",
  "alternatives": [
    {"source": "BBC", "title": "Real Story...", "url": "..."}
  ]
}
```

## 📂 Project Structure

*   `graph.py`: Main LangGraph workflow logic.
*   `tools/`: Helper modules (Perplexity, Search, FactCheck, Extraction).
*   `frontend.py`: Streamlit User Interface.
*   `app.py`: FastAPI backend endpoints.
*   `trace_workflow.py`: CLI tool for debugging/tracing.

## ⚖️ Limitations

*   **Political Nuance**: Highly complex political claims may sometimes return "UNCERTAIN" to avoid hallucinations.
*   **Regional News**: Best performance is on major international or English-language news.
