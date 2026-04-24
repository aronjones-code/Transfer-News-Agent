import streamlit as st
from google import genai
from google.genai import types

# 1. Page Styling
st.set_page_config(page_title="United Scout", page_icon="🔴")
st.title("🔴 MUFC Transfer Scout")
st.write("Scans the latest rumors and ranks them for the 2026 Carrick system.")

# 2. Key Input
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    if st.button("Generate Morning Report"):
        with st.spinner("Searching for Fabrizio Romano, The Athletic, and news feeds..."):
            
            # The Agent's Logic
            prompt = """
            Find the top 5 most recent Manchester United transfer rumors from the last 24 hours.
            Rank them based on fit for Michael Carrick's 2026 system:
            - Focus: Technical pivots (Mainoo style), inverted wingbacks, and roaming #10s.
            - Provide: Player name, rumored fee, tactical fit, and a verdict (Strong Buy/Avoid).
            """
            
            # Executing the search + reasoning
            response = client.models.generate_content(
                model="gemini-3-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            
            st.markdown(response.text)
else:
    st.info("Enter your API Key in the sidebar to start.")
