import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

genai.configure(api_key='AIzaSyD7VFEhltOsCDi5GJLMqNIyqDWg0g2Julo')
model = genai.list_models()
for model in model:
    print(model)
llm = GoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key='AIzaSyD7VFEhltOsCDi5GJLMqNIyqDWg0g2Julo',
                         temperature=1.0)
nutritional_info_template = PromptTemplate(
    input_variables=["food_items"],
    prompt_template="""provide detailed nutritionale following food items: {food_items}.
    Include macronutrients (protein, fat, carbohydrates), micronutrients(vitamins, minerals), and calorie content."""
)


def get_food_items_input():
    with st.form("food_items_input_form"):
         food_items = st.text_area("Enter food items (separate by commas):", "")
         submitted = st.form_submit_button("Get Nutritional Information")
    if submitted:
     return {"food_items": food_items}

def get_nutritional_info_response(input_data):


    if input_data is None:
      return "Error: No food items provided."
    prompt = nutritional_info_template.format(**input_data)
    response = llm(prompt)
    return response
st.title("NutriAI - Instant Nutritional Information")
input_data = get_food_items_input()
if input_data:
    with st.spinner("Fetching Nutritional Information..."):
        response = get_nutritional_info_response(input_data)
st.subheader("Nutritional Information")
st.write(response)
