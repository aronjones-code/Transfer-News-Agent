import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="United Scout", page_icon="🔴")
st.title("🔴 MUFC Transfer Scout")

raw_key = st.sidebar.text_input("Gemini API Key", type="password")
api_key = raw_key.strip() 

if api_key:
    # 1. Setup the client with a longer timeout
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30000) # 30 seconds
    )
    
    if st.button("Generate Morning Report"):
        report_placeholder = st.empty()
        with st.spinner("Agent is searching (this may take a minute if servers are busy)..."):
            
            # 2. Configure 'Automatic Retries'
            # This tells the agent: "If the server is busy (503), try again up to 10 times"
            retry_config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                http_options=types.HttpOptions(
                    retry_options=types.HttpRetryOptions(
                        attempts=10,
                        initial_delay=2.0,
                        max_delay=60.0,
                        http_status_codes=[503, 429]
                    )
                )
            )

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents="Find the top 5 Man Utd transfer rumours from the last 24 hours. Rank for Carrick's system.",
                    config=retry_config
                )
                report_placeholder.markdown(response.text)
                st.success("Scouting complete!")
                
            except Exception as e:
                if "503" in str(e):
                    st.error("Google's servers are currently overloaded. This is common during peak morning hours in the UK. Please wait 5 minutes and try again.")
                else:
                    st.error(f"Agent snagged: {e}")
else:
    st.info("Paste your API Key in the sidebar.")
