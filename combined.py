# import streamlit as st
# import openai
# import os
# from dotenv import load_dotenv

# # Load API key
# load_dotenv()
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable
# client = wrap_openai(openai.Client())
# # Load prompt
# try:
#     with open("combined prompt.txt", "r", encoding="utf-8") as f:
#         base_prompt = f.read()
# except Exception as e:
#     st.error(f"❌ Failed to load prompt: {e}")
#     st.stop()

# # Streamlit UI
# st.set_page_config(page_title="Dental Template Generator", layout="centered")
# st.title("🦷 Dental Template Generator")

# raw_input = st.text_area("📝 Clinical Text", height=200)

# if st.button("Generate Template"):
#     if not raw_input.strip():
#         st.warning("⚠️ Please enter a clinical paragraph first.")
#     else:
#         with st.spinner("genrating"):
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": base_prompt},
#                         {"role": "user", "content": raw_input}
#                     ],
#                     temperature=0.5,
#                     top_p=0.95,
#                     max_tokens=1024
#                 )

#                 output_text = response.choices[0].message.content.strip()
#                 st.success("✅ Generated Dental Template:")
#                 st.text_area("🦷 Treatment Note", value=output_text, height=300)

#             except Exception as e:
#                 st.error(f"❌ OpenAI API error: {e}")


import streamlit as st
import openai
import os
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# Load environment variables
load_dotenv()
client = wrap_openai(openai.Client())

# Load prompt
try:
    with open("combined prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read()
except Exception as e:
    st.error(f"❌ Failed to load prompt: {e}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="Dental Template Generator", layout="centered")
st.title("🦷 Dental Template Generator")

raw_input = st.text_area("📝 Clinical Text", height=200)

# ---- Traceable OpenAI Wrapper ----
@traceable
def generate_dental_template(user_input: str):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5,
        top_p=0.95,
        max_tokens=1024
    )

# ---- Button Trigger ----
if st.button("Generate Template"):
    if not raw_input.strip():
        st.warning("⚠️ Please enter a clinical paragraph first.")
    else:
        with st.spinner("⏳ Generating template..."):
            try:
                response = generate_dental_template(raw_input)
                output_text = response.choices[0].message.content.strip()
                st.success("✅ Generated Dental Template:")
                st.text_area("🦷 Treatment Note", value=output_text, height=300)
            except Exception as e:
                st.error(f"❌ OpenAI API error: {e}")
