import streamlit as st
from PIL import Image
from google import genai
import json, re

# Gemini client setup
client = genai.Client(api_key=st.secrets["gemini_key"])

# ------------------------------
# Gemini Math Reasoning Pipeline (Image or Text)
# ------------------------------
def solve_with_gemini(input_type, input_data):
    if input_type == "image":
        prompt = """
You are a math tutor. Given an image that contains a math problem (printed or handwritten), perform the following:
1. Extract the math question from the image.
2. Detect the language.
3. If the question is a valid math/reasoning/logical problem:
   - Translate it into English.
   - Solve it step-by-step using clear reasoning.
   - Provide the final answer wrapped in \boxed{}.
4. If it is NOT a valid math question, return this JSON:
{
  "status": "error",
  "reason": "Not a math problem."
}
5. If valid, respond with this JSON:
{
  "status": "ok",
  "original_language": "<language>",
  "solution": "<Step-by-step solution with answer in \\boxed{}>",
  "translated_question": "<MathQuestion in English>"
}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[prompt, input_data]
        )
        return response

    elif input_type == "text":
        prompt = f"""
You are a math tutor. Follow these instructions:
1. Detect the language of this input.
2. If it's a math/reasoning/logical question:
   - Translate to English.
   - Solve it step-by-step clearly.
   - Put the final answer inside \boxed{}.
3. If not valid, respond:
{{"status": "error", "reason": "Not a math problem."}}
4. If valid, respond:
{{
  "status": "ok",
  "original_language": "<language>",
  "solution": "<Step-by-step solution with answer in \\boxed{}>",
  "translated_question": "<MathQuestion in English>"
}}

Input:
{input_data}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="MatriMath - AI Math Assistant", layout="centered", page_icon="📐")
st.title("🧠 MatriMath: Multilingual Math Assistant (Gemini-only)")

uploaded_file = st.file_uploader("📸 Upload an image with a math problem (handwritten or printed)", type=["jpg", "jpeg", "png"])
user_text = st.text_area("📝 Or type your math question:", "")

if st.button("🚀 Solve It"):
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        with st.spinner("🔍 Gemini is analyzing the image and solving..."):
            response = solve_with_gemini("image", image)
    elif user_text.strip():
        with st.spinner("🧠 Gemini is analyzing your text and solving..."):
            response = solve_with_gemini("text", user_text)
    else:
        st.warning("Please upload an image or enter a question.")
        st.stop()

    try:
        result_json = json.loads(re.search(r"{.*}", response.text, re.DOTALL)[0])

        if result_json["status"] == "error":
            st.error("🚫 Not a valid math or reasoning question.")
        else:
            st.markdown("### 📘 Translated Math Question (English):")
            st.info(result_json["translated_question"])

            st.markdown("### 🧾 Step-by-step Solution:")
            st.success(result_json["solution"])

    except Exception as e:
        st.error(f"⚠️ Failed to parse Gemini response.\n{e}")
