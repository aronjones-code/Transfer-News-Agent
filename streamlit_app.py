import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="United Scout", page_icon="🔴")
st.title("🔴 MUFC Transfer Scout")

raw_key = st.sidebar.text_input("Gemini API Key", type="password")
api_key = raw_key.strip() 

if api_key:
    # 1. Setup client with a 120-second timeout (Crucial for 2026 Search)
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000) 
    )
    
    if st.button("Generate Morning Report"):
        report_placeholder = st.empty()
        with st.spinner("Scouting today's news... (The agent is currently reading live articles)"):
            
            # 2. Optimized Prompt for 2026 speed
            prompt = """
            Search for the top 3 latest Man Utd transfer rumours from today.
            Focus on Fabrizio Romano or The Athletic.
            Summarize the fit for a technical 4-2-3-1 system.
            Keep the report concise to avoid server timeouts.
            """

            try:
                # 3. Switching to Gemini 3 Flash for maximum speed
                response = client.models.generate_content(
                    model="gemini-3-flash-preview", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        http_options=types.HttpOptions(
                            retry_options=types.HttpRetryOptions(
                                attempts=5,
                                http_status_codes=[503, 504]
                            )
                        )
                    )
                )
                report_placeholder.markdown(response.text)
                st.success("Scouting report delivered!")
                
            except Exception as e:
                st.error(f"Agent snagged: {e}")
                st.info("💡 Tip: If you still get a timeout, try clicking the button one more time. The agent 'caches' its search results and often works on the second try.")
else:
    st.info("Paste your API Key in the sidebar.")
