import streamlit as st
import json
from graph import graph

st.set_page_config(page_title="Misinformation Verification Agent", layout="wide")

st.title("🕵️‍♂️ Misinformation Verification Agent")
st.markdown("Enter a news article or headline below to verify its authenticity using strict fact-checking protocols.")

# Input Section
input_text = st.text_area("Article Content / Headline", height=150, placeholder="Paste the text here...")

if st.button("Verify Article", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing... Extracting headline, searching, and fact-checking..."):
            # Invoke Graph
            try:
                state = {
                    "article_text": input_text,
                    "headline": "" # Let the agent extract it
                }
                result = graph.invoke(state)
                
                # Extract Results
                headline = result.get("headline", "N/A")
                verdict = result.get("verdict", "UNCERTAIN")
                confidence = result.get("confidence", "0%")
                summary = result.get("summary", "No summary available.")
                alternatives = result.get("alternatives", [])
                original_language = result.get("original_language", "en")
                original_text = result.get("original_text", "")
                translated_text = result.get("article_text", "")
                
                # Layout Results
                st.divider()
                
                # Translation Display
                if original_language and original_language != "en" and original_language != "unknown":
                    st.warning(f"🌐 Translated from **{original_language.upper()}**")
                    with st.expander("View Translated Text (English)"):
                        st.write(translated_text)
                
                st.subheader("Analysis Results")
                
                # Metrics Row
                col1, col2 = st.columns(2)
                
                with col1:
                    st.caption("Extracted Headline")
                    st.info(headline)
                    
                with col2:
                    st.caption("Verdict")
                    if verdict == "SAFE TO PROCEED":
                        st.success(f"✅ {verdict}")
                    elif verdict == "POTENTIAL MISINFORMATION":
                        st.error(f"🚨 {verdict}")
                    else:
                        st.warning(f"⚠️ {verdict}")
                    st.metric("Confidence Score", confidence)

                # Summary Section
                st.subheader("Summary")
                st.write(summary)
                
                # Alternatives Section (Only if Misinfo or Uncertain)
                if alternatives:
                    st.subheader("Trusted Alternatives")
                    for alt in alternatives:
                        with st.expander(f"{alt.get('source', 'Unknown Source')}: {alt.get('title', 'Article')}"):
                            st.write(f"**Source:** {alt.get('source', 'Unknown')}")
                            st.write(f"[Read Article]({alt.get('url', '#')})")
                elif verdict == "POTENTIAL MISINFORMATION":
                    st.info("No specific alternative articles found, but the claim is flagged as misinformation.")

                # Raw Output Expander for debugging
                with st.expander("View Raw JSON Output"):
                    output_json = {
                        "headline": headline,
                        "verdict": verdict,
                        "confidence": confidence,
                        "summary": summary,
                        "alternatives": alternatives
                    }
                    st.json(output_json)
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
