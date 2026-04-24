import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="United Scout", page_icon="🔴")
st.title("🔴 MUFC Transfer Scout")

raw_key = st.sidebar.text_input("Gemini API Key", type="password")
api_key = raw_key.strip() 

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if st.button("Generate Morning Report"):
            with st.spinner("Agent is scouring the web..."):
                
                # 2026 PROMPT: More specific to ensure high-quality scouting
                prompt = """
                Search for the top 5 Manchester United transfer rumours from the last 24 hours.
                Focus on reputable sources like The Athletic, Fabrizio Romano, and Tier 1 BBC.
                Rank them for Michael Carrick's 4-2-3-1 'Technical Pivot' system.
                For each: Player name, Source, Fee, and 'Carrick Fit Score' (1-10).
                """

                # Using 'gemini-2.5-flash' - the 2026 GA standard for Tools
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                st.markdown(response.text)
                st.success("Report Generated successfully.")
                
    except Exception as e:
        # Clearer error messaging for common 2026 hurdles
        error_msg = str(e)
        if "404" in error_msg:
            st.error("Model Not Found: Please check your model version in the code.")
        elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            st.error("Quota full! Wait 60 seconds or check your Google Cloud Billing.")
        else:
            st.error(f"Agent Error: {error_msg}")
else:
    st.info("Paste your API Key (starting with AIza) in the sidebar.")
