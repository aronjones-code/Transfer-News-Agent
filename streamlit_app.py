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
            with st.spinner("Searching the web for United rumours..."):
                
                # Using 1.5-flash as it is currently the most reliable for UK-based search grounding
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents="Search for the 3 biggest Man Utd transfer rumours from the last 24 hours. Rank them for a technical 4-2-3-1 system.",
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                st.markdown(response.text)
                
    except Exception as e:
        # This will now give you a clearer explanation of the error
        st.error(f"Agent Error: {e}")
        if "limit: 0" in str(e):
            st.warning("💡 **UK Region Detected:** Please ensure you have linked a Billing Account in Google Cloud Console to unlock your free quota.")
else:
    st.info("Paste your API Key (starting with AIza) in the sidebar.")
