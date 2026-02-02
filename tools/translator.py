from langdetect import detect, LangDetectException
from transformers import MarianMTModel, MarianTokenizer
import logging

# Configure logging to avoid spamming console
logging.getLogger("transformers").setLevel(logging.ERROR)

_model = None
_tokenizer = None
MODEL_NAME = "Helsinki-NLP/opus-mt-mul-en"

def get_model_and_tokenizer():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        print(f"Loading translation model ({MODEL_NAME})...")
        try:
            _tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
            _model = MarianMTModel.from_pretrained(MODEL_NAME)
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e
    return _model, _tokenizer

def translate_content(text: str) -> dict:
    """
    Detects language and translates to English if necessary.
    Returns: {"translated_text": str, "original_language": str, "original_text": str}
    """
    if not text or not text.strip():
        return {"translated_text": "", "original_language": "unknown", "original_text": ""}

    # 1. Detect Language
    try:
        lang = detect(text)
    except LangDetectException:
        lang = "unknown"

    # 2. If already English, skip
    if lang == "en":
        return {
            "translated_text": text,
            "original_language": "en",
            "original_text": text
        }

    # 3. Translate
    try:
        model, tokenizer = get_model_and_tokenizer()
        
        # Prepare inputs
        # Truncate to 512 tokens
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Generate translation
        generated_tokens = model.generate(**inputs)
        translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        
        return {
            "translated_text": translated_text,
            "original_language": lang,
            "original_text": text
        }
    except Exception as e:
        print(f"Translation logic error: {e}")
        return {
            "translated_text": text, # Fallback to original
            "original_language": lang,
            "original_text": text,
            "error": str(e)
        }
