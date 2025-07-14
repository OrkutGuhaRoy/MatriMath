
# 🧠 MatriMath – Multilingual Math Assistant

![Banner](https://img.shields.io/badge/Gemini%202.5%20Pro-Google-brightgreen) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange) ![Status](https://img.shields.io/badge/Status-Experimental-yellow)

MatriMath is a multilingual AI math assistant built using **Google Gemini 2.5 Pro** that allows users to input math or reasoning problems in **any language** — and receive:

* 🗣️ A **step-by-step solution** in the **original language**
* 📘 The same solution in **English**
* 🎓 Both **Feynman-style intuitive explanations** and **technical breakdowns**

---

## ✨ Features

* 📸 Upload **printed or handwritten** math problems as images
* 📝 Or type your question directly — in **any language**
* 🔁 **Language detection**, **translation**, and **solution generation** handled by Gemini
* 🎯 Dual explanations:

  * Feynman-style, relatable explanation with **Indian/Indic examples**
  * Rigorous, technical solution with formulas
* 🌐 Final solution returned in **both English and the original language**

---

## 🔍 Why the name *MatriMath*?

“**Matri**” means *mother*.

Just like your mother patiently teaches you in your mother tongue, MatriMath helps you learn math in a nurturing way — in your own language, with step-by-step clarity.

---

## 💡 Ideal Use Cases

* Students in **regional-medium schools** preparing for exams like **WBJEE, NEET, JEE, etc.**
* Learners who want to understand **math concepts better** in their **native language**
* Anyone struggling with **math problem statements in English**

---

## 🖥️ Tech Stack

* 🧠 [Gemini 2.5 Pro]((https://ai.google.dev/gemini-api/docs/models#gemini-2.5-pro))
* 🧰 Python
* 🌐 [Streamlit](https://streamlit.io/)
* 📦 PIL, `re`, `json`

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/matrimath.git
cd matrimath

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key to Streamlit secrets
mkdir .streamlit
echo '[gemini_key]\ngemini_key = "YOUR_GEMINI_API_KEY"' > .streamlit/secrets.toml

# Launch the app
streamlit run streamlit_app.py
```

---

## 📬 Contact

Have feedback or want to collaborate?
Reach out: **[swastikguharoy@googlemail.com](mailto:swastikguharoy@googlemail.com)**

---

## ⚠️ Disclaimer

This app is an educational prototype.
Solutions are AI-generated — **verify before relying on them for critical use**.

---
