import streamlit as st
from google import genai
from google.genai import types

# 1. Page Styling
st.set_page_config(page_title="United Scout", page_icon="🔴")
st.title("🔴 MUFC Transfer Scout")

# 2. Key Input - Added .strip() to automatically remove accidental spaces
raw_key = st.sidebar.text_input("Gemini API Key", type="password")
api_key = raw_key.strip() 

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if st.button("Generate Morning Report"):
            with st.spinner("Searching the web for United rumours..."):
                
                # Changed to gemini-2.0-flash for maximum stability with the Search tool
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents="Find the top 5 Man Utd transfer rumours from the last 24 hours. Rank them for Carrick's 2026 system.",
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"The Agent hit a snag: {e}")
else:
    st.info("Paste your API Key in the sidebar. (Make sure it starts with AIza...)")
