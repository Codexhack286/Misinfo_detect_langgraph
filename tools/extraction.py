from llm import llm

def extract_headline(article_text: str) -> str:
    """
    Extracts the exact headline from the given article text using an LLM.
    """
    prompt = (
        "Extract the exact headline from the following news article text. "
        "Return ONLY the headline, nothing else.\n\n"
        f"Article:\n{article_text}"
    )
    result = llm.invoke(prompt)
    return result.content.strip()
