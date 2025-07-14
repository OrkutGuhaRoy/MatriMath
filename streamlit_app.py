    import streamlit as st
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from PIL import Image
    from google import genai
    import json, re

torch.random.manual_seed(0)

client=genai.Client(api_key=st.secrets["gemini_key"])

# ------------------------------
# Gemini Prompt Engineer (Image or Text)
# ------------------------------
def refine_with_gemini(input_type, input_data):
    if input_type == "image":
        prompt = """
You are a mathematical prompt engineer.

Given an image containing a math question (e.g., a handwritten or printed problem):
1. Extract the text from the image.
2. Detect the language.
3. If it's a valid math/reasoning/logical question:
   - Translate it into English.
   - Format it as:
     <|user|><MathQuestion in English>\nPlease reason step by step, and put your final answer within \\boxed{{}}.<|end|><|assistant|>
4. If it's NOT a valid math/reasoning question, respond with this JSON:
{
  "status": "error",
  "reason": "Not a mathematical/logical reasoning question."
}
5. If valid, respond with this JSON:
{
  "status": "ok",
  "original_language": "<language>",
  "formatted_prompt": "<|user|>...<|end|><|assistant|>"
}
"""        
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents= [prompt, input_data])
        return response.text

    elif input_type == "text":
        gemini_prompt = f"""
You are a mathematical prompt engineer.
Your job is to:
1. Detect the language of the input.
2. Check if the query is appropriate for a math reasoning model.
3. If valid, translate it into English.
4. Format it as:
     <|user|><MathQuestion in English>\nPlease reason step by step, and put your final answer within \\boxed{{}}.<|end|><|assistant|>

If the question is **not** a math/reasoning/logical problem, return this JSON:
{{
  "status": "error",
  "reason": "Not a mathematical/logical reasoning question."
}}

If it is a valid question, return this JSON:
{{
  "status": "ok",
  "original_language": "<language>",
  "formatted_prompt": "<|user|>...<|end|><|assistant|>"
}}

Input:
{input_data}
"""
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents= [prompt, input_data])
        return response.text

# ------------------------------
# Load Phi-4 Model
# ------------------------------
@st.cache_resource
def load_phi():
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-math-7b-base")
    model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/deepseek-math-7b-base",
        device_map="auto",
        torch_dtype="torch.bfloat16",
    )
    return tokenizer, model

# ------------------------------
# Run Phi Model
# ------------------------------
def run_deepseek(prompt):
    tokenizer, model = load_phi()
    messages = [{"role": "user", "content": prompt}]
    
    input_text = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_dict=False,  # 👈 return plain string for manual tokenization
    )
    
    inputs = tokenizer(
        input_text,
        return_tensors="pt"
    ).to(model.device)  # ✅ this is now a tensor dictionary on correct device

    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        temperature=0.6,
        top_p=0.95,
        do_sample=True,
    )

    decoded = tokenizer.batch_decode(outputs[:, inputs["input_ids"].shape[-1]:])
    return decoded[0]


# ------------------------------
# UI
# ------------------------------
st.set_page_config(page_title="MatriMath - AI Math Assistant", layout="centered", page_icon="📐")
st.title("🧠 MatriMath: Multilingual Math Assistant")

uploaded_file = st.file_uploader("📸 Upload an image containing a math problem (printed or handwritten)", type=["jpg", "jpeg", "png"])
user_text = st.text_area("📝 Or type your math question here:", "")

if st.button("🚀 Solve It"):
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        with st.spinner("🔧 Gemini is processing the image..."):
            response = refine_with_gemini("image", image)
    elif user_text.strip():
        with st.spinner("🔧 Gemini is processing your text..."):
            response = refine_with_gemini("text", user_text)
    else:
        st.warning("Please upload an image or type a question.")
        st.stop()

    if '"status": "error"' in response:
        st.error("🚫 Not a valid math or reasoning question.")
    else:
        try:
            response_json = json.loads(re.search(r'{.*}', response, re.DOTALL)[0])
            prompt_for_phi = response_json["formatted_prompt"]
            original_lang = response_json["original_language"]

            with st.spinner("🧠 Solving with deepseek-math-7b-base..."):
                answer = run_deepseek(prompt_for_phi)

            with st.spinner("🌐 Translating back to original language..."):
                back_prompt = f"Translate this into {original_lang} preserving clarity: \n{answer}"
                translated = client.models.generate_content(
                model="gemini-2.5-flash", contents= back_prompt).text

            st.markdown("### 🧾 Answer in your language:")
            st.success(translated)

            st.markdown("### 📘 English Answer:")
            st.info(answer)

        except Exception as e:
            st.error(f"⚠️ Failed to parse Gemini response.\n{e}")
