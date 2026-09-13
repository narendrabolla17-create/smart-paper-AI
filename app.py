import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Paper AI", page_icon="🎓", layout="centered")

st.title("🎓 Smart Paper AI")
st.subheader("GEC Students Co-AI Exam Assistant")

# Initialize GenAI Client securely using Streamlit Secrets
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key configuration missing in Streamlit Secrets. Please configure it.")
    client = None

# Sidebar inputs for a clean professional look
st.sidebar.header("⚙️ యాప్ సెట్టింగ్స్")

subject = st.sidebar.selectbox(
    "సబ్జెక్ట్ ఎంచుకో:", 
    ["C Programming", "Python Programming", "Internet of Things (IoT)", "Data Structures"]
)

difficulty = st.sidebar.selectbox(
    "డిఫికల్టీ లెవెల్:", 
    ["Easy", "Medium", "Hard"]
)

show_answers = st.sidebar.checkbox("✅ యాన్సర్ కీ / సొల్యూషన్స్ కావాలి", value=True)

# Main content area
topic = st.text_input("Topic పేరు టైప్ చేయి (eg: Arrays, Sensors, Loops):")

if client:
    if st.button("📄 Paper జెనరేట్ చేయి"):
        if not topic.strict() if hasattr(topic, 'strict') else not topic.strip():
            st.warning("దయచేసి టాపిక్ పేరు రాయండి!")
        else:
            with st.spinner("AI ఎగ్జామ్ పేపర్ తయారు చేస్తోంది... వేచి ఉండండి 🚀"):
                answer_instruction = "Include detailed answers and explanations for the questions." if show_answers else "Provide only questions without answers."
                
                prompt = (
                    f"Act as an expert professor. Generate a comprehensive exam paper and study guide for "
                    f"the subject '{subject}' with '{difficulty}' difficulty level, specifically focused on the topic '{topic}'. "
                    f"Include a clear concept summary and 5 important short questions. {answer_instruction} "
                    f"Provide simple Telugu explanations alongside English technical terms."
                )
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
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
