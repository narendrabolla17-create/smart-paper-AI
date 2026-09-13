import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Paper AI", page_icon="🎓", layout="centered")

st.title("🎓 Smart Paper AI")
st.subheader("GEC Students Co-AI Exam Assistant")

# API Key input
api_key = st.text_input("Google AI Studio API Key ఇక్కడ పెట్టు:", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        # Layout columns for Subject and Difficulty
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox(
                "సబ్జెక్ట్ ఎంచుకో:", 
                ["C Programming", "Python Programming", "Internet of Things (IoT)", "Data Structures"]
            )
        with col2:
            difficulty = st.selectbox(
                "డిఫికల్టీ లెవెల్:", 
                ["Easy", "Medium", "Hard"]
            )
            
        topic = st.text_input("Topic పేరు టైప్ చేయి (eg: Arrays, Sensors, Loops):")

        if st.button("📄 Paper జెనరేట్ చేయి"):
            if not topic.strip():
                st.warning("దయచేసి టాపిక్ పేరు రాయండి!")
            else:
                with st.spinner("AI ఎగ్జామ్ పేపర్ తయారు చేస్తోంది... వేచి ఉండండి 🚀"):
                    prompt = (
                        f"Act as an expert professor. Generate a comprehensive exam paper and study guide for "
                        f"the subject '{subject}' with '{difficulty}' difficulty level, specifically focused on the topic '{topic}'. "
                        f"Include a clear concept summary and 5 important short questions with answers, providing simple Telugu explanations alongside English technical terms."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    paper_content = response.text
                    
                    st.success("✨ నీ Smart Paper సిద్ధంగా ఉంది!")
                    st.markdown(paper_content)
                    
                    # Download Button
                    st.download_button(
                        label="📥 Download Paper as File",
                        data=paper_content,
                        file_name=f"{subject}_{topic}_Exam_Paper.txt",
                        mime="text/plain"
                    )
    except Exception as e:
        st.error(f"ఎర్రర్ వచ్చింది: {e}")
else:
    st.info("దయచేసి పైన మీ Google AI Studio API Key ఎంటర్ చేయండి.")
