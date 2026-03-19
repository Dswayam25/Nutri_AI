import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# 🔐 Load API key securely
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

# Initialize LLM
llm = GoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=api_key,
    temperature=1.0
)

# Prompt template
nutritional_info_template = PromptTemplate(
    input_variables=["food_items"],
    template="""
Provide detailed nutritional information for the following food items: {food_items}.

Include:
- Calories
- Macronutrients (protein, fat, carbohydrates)
- Key vitamins
- Minerals
- Keep response clean and structured
"""
)

# UI Input
def get_food_items_input():
    with st.form("food_items_input_form"):
        food_items = st.text_area(
            "Enter food items (separate by commas):",
            placeholder="e.g. rice, chicken, banana"
        )
        submitted = st.form_submit_button("Get Nutritional Information")

    if submitted and food_items.strip():
        return {"food_items": food_items}
    return None

# Generate response
def get_nutritional_info_response(input_data):
    prompt = nutritional_info_template.format(**input_data)
    response = llm.invoke(prompt)
    return response

# UI Layout
st.set_page_config(page_title="NutriAI", page_icon="🥗")

st.title("🥗 NutriAI - Instant Nutritional Information")

input_data = get_food_items_input()

if input_data:
    with st.spinner("Analyzing nutrition..."):
        response = get_nutritional_info_response(input_data)

    st.subheader("📊 Nutritional Information")
    st.write(response)
else:
    st.info("Enter food items to get started.")
