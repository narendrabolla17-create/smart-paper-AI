import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Paper AI", page_icon="🎓")
st.title("🎓 Smart Paper AI")
st.caption("GEC Students కోసం AI Exam Assistant")

api_key = st.text_input("Google AI Studio API Key ఇక్కడ పెట్టు:", type="password")
subject = st.selectbox("Subject ఎంచుకో:", ["C Programming", "Basic Electrical Engineering (EEE)", "IoT Basics", "Other"])
topic = st.text_input("Topic పేరు టైప్ చెయ్ (eg: Arrays or Ohm's Law):")

if st.button("🚀 Paper జనరేట్ చెయ్"):
    if not api_key or not topic:
        st.warning("API Key మరియు Topic రెండూ టైప్ చేయి బాస్!")
    else:
        with st.spinner("AI నోట్స్ తయారు చేస్తోంది..."):
            client = genai.Client(api_key=api_key)
            prompt = f"Subject: {subject}, Topic: {topic}. Provide 5 important short questions with answers and detailed concept summary with simple Telugu explanation."
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            st.success("✨ నీ Smart Paper సిద్ధంగా ఉంది!")
            st.write(response.text)