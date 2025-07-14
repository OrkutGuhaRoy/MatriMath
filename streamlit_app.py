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
   - Solve it step-by-step.
   - Your explanation must contain:
     a) A simple, Feynman-style explanation using relatable, real-world analogies or examples in an Indian/Indic setting.
     b) A technical breakdown that includes necessary mathematical concepts and formulas.
   - Clearly mark the final answer as: Final Answer: <your answer>
4. If it is NOT a valid math question, return this JSON:
{
  "status": "error",
  "reason": "Not a math problem."
}
5. If valid, respond with this JSON:
{
  "status": "ok",
  "original_language": "<language>",
  "solution": "<Step-by-step solution with Final Answer>",
  "translated_question": "<MathQuestion in English>"
}
"""
        response = client.models.generate_content(
            model="gemini-2.5-pro", contents=[prompt, input_data]
        )
        return response

    elif input_type == "text":
        prompt = f"""
You are a math tutor. Follow these instructions:
1. Detect the language of this input.
2. If it's a math/reasoning/logical question:
   - Translate to English.
   - Solve it step-by-step.
   - Your explanation must contain:
     a) A simple, Feynman-style explanation using relatable, real-world analogies or examples in an Indian/Indic setting.
     b) A technical breakdown that includes necessary mathematical concepts and formulas.
   - Clearly mark the final answer as: Final Answer: <your answer>
3. If not valid, respond:
{{"status": "error", "reason": "Not a math problem."}}
4. If valid, respond:
{{
  "status": "ok",
  "original_language": "<language>",
  "solution": "<Step-by-step solution with Final Answer>",
  "translated_question": "<MathQuestion in English>"
}}

Input:
{input_data}
"""
        response = client.models.generate_content(
            model="gemini-2.5-pro", contents=prompt
        )
        return response

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="MatriMath - AI Math Assistant", layout="centered", page_icon="📐")
st.title("🧠 MatriMath: Multilingual Math Assistant (Powered by Gemini 2.5 Pro)")
with st.expander("ℹ️ About MatriMath"):
    st.markdown("""
**👤 Created by:** `Swastik Guha Roy`  
**🔧 Powered by:** Google Gemini 2.5 Pro API  

---

### 🌟 What is MatriMath?

Imagine an app where you can ask a math or logical reasoning question — in **any language you're comfortable with** — and get a **step-by-step explanation** in both:

- ✨ **English**  
- 🗣️ **Your original language**

You don’t have to worry about fluency in English or crafting the perfect prompt. Just input your question (typed or via image), and MatriMath takes care of the rest — from language detection to solution explanation.

---

### 💖 Why the name *MatriMath*?

“**Matri**” means *mother*.

Just like your mother patiently helped you learn things step-by-step — in your own language — MatriMath aims to teach math in a way that’s nurturing, clear, and comforting.  
You’ll get both:

- A **Feynman-style, intuitive explanation** using real-world examples  
- A **technically complete** breakdown of the concepts involved

---

### ⚠️ Disclaimer

- This is an experimental educational tool.  
- Accuracy of solutions is **not guaranteed**.  
- Always cross-check critical answers manually.

---

### 📬 Contact

Have suggestions, feedback, or want to collaborate?  
Reach out: **swastikguharoy@googlemail.com**
    """)

    with st.expander("🌐 বাংলা ভাষায়"):
        st.markdown("""
**👤 নির্মাতা:** `স্বস্তিক গুহ রায়`  
**🔧 চালিত হয়েছে:** Google Gemini 2.5 Pro API দ্বারা  

---

### 🌟 MatriMath কী?

ভাবুন, এমন একটি অ্যাপ যেখানে আপনি যেকোনো ভাষায় গণিত বা যুক্তির প্রশ্ন করতে পারেন,  
আর সেই প্রশ্নের **ধাপে ধাপে সমাধান** পাবেন:

- ✨ **ইংরেজিতে**  
- 🗣️ **আপনার নিজের ভাষায়**  

ইংরেজি জানতেই হবে—এই চাপটা আর থাকবে না।  
প্রশ্ন দিন, বাকিটা MatriMath নিজেই বুঝে নেবে এবং ব্যাখ্যা দেবে।

---

### 💖 নাম *MatriMath* কেন?

“**মাতৃ**” মানে মা। 

যেভাবে আপনার মা ধৈর্য ধরে শিখিয়েছেন ছোটবেলায়,  
MatriMath-ও সেইভাবেই নিজের ভাষায় সহজ উদাহরণে গণিত বোঝাবে।  

আপনি পাবেন—

- **সাধারণ উদাহরণে ব্যাখ্যা**  
- **সঠিক সূত্র, ধাপ ও প্রযুক্তিগত বিশ্লেষণসহ সমাধান**

---

### ⚠️ দায়িত্ব অস্বীকার

- এটি একটি পরীক্ষামূলক শিক্ষামূলক টুল।  
- সঠিকতার গ্যারান্টি নেই।  
- গুরুত্বপূর্ণ গণনাগুলি নিজে যাচাই করে নিন।

---

### 📬 যোগাযোগ করুন

মতামত, পরামর্শ, অথবা সহযোগিতার জন্য —  
**swastikguharoy@googlemail.com** এ মেইল করুন।
""")


uploaded_file = st.file_uploader("📸 Upload an image with a math problem (handwritten or printed)", type=["jpg", "jpeg", "png"])
user_text = st.text_area("📝 Or type your math question:", "")

if st.button("🚀 Solve It"):
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        with st.spinner("🔍 Analyzing the image and solving..."):
            response = solve_with_gemini("image", image)
    elif user_text.strip():
        with st.spinner("🧠 Analyzing your text and solving..."):
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

            with st.spinner("🌐 Translating solution back to original language..."):
                back_prompt = f"""Translate the following step-by-step math solution into {result_json['original_language']}:

{result_json['solution']}"""
                translated_solution = client.models.generate_content(
                    model="gemini-2.5-flash", contents=back_prompt
                ).text

            st.markdown("### 🌍 Solution in Your Language:")
            st.success(translated_solution)

            st.markdown("### 🧾 English Step-by-step Solution:")
            st.info(result_json["solution"])

    except Exception as e:
        st.error(f"⚠️ Failed to parse Gemini response.\n{e}")
