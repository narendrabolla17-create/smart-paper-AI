import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Smart Paper AI", page_icon="🎓", layout="centered")

st.title("🎓 Smart Paper AI")
st.subheader("GEC Students Co-AI Exam Assistant")

# Sidebar settings
st.sidebar.header("App Settings")

# Check Streamlit Secrets first, otherwise fallback to sidebar text input
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = st.sidebar.text_input("Google AI Studio API Key:", type="password")

subject = st.sidebar.selectbox(
    "Select Subject:", 
    ["C Programming", "Python Programming", "Internet of Things (IoT)", "Data Structures"]
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level:", 
    ["Easy", "Medium", "Hard"]
)

show_answers = st.sidebar.checkbox("Include Answer Key / Solutions", value=True)

# Main content area
topic = st.text_input("Enter Topic Name (eg: Arrays, Sensors, Loops):")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        if st.button("Generate Paper"):
            if not topic.strip():
                st.warning("Please enter a topic name!")
            else:
                with st.spinner("AI is generating the exam paper... Please wait 🚀"):
                    answer_instruction = "Include detailed answers and explanations for the questions." if show_answers else "Provide only questions without answers."
                    
                    prompt = (
                        f"Act as an expert professor. Generate a comprehensive exam paper and study guide for "
                        f"the subject '{subject}' with '{difficulty}' difficulty level, specifically focused on the topic '{topic}'. "
                        f"Include a clear concept summary and 5 important short questions. {answer_instruction} "
                        f"Provide clear explanations alongside technical terms."
                    )
                    
                    response = model.generate_content(prompt)
                    paper_content = response.text
                    
                    st.success("Your Smart Paper is ready!")
                    st.markdown(paper_content)
                    
                    # Download Button
                    st.download_button(
                        label="Download Paper as File",
                        data=paper_content,
                        file_name=f"{subject}_{topic}_Exam_Paper.txt",
                        mime="text/plain"
                    )
    except Exception as e:
        st.error(f"Error Details: {e}")
else:
    st.info("Please enter your Google AI Studio API Key in the sidebar or configure it in Streamlit Secrets.")
