import os
from groq import Groq
import streamlit as st
import random

# ------------------------------------------------------------------
# ⚡ GROQ ENGINE (Secure)
# ------------------------------------------------------------------
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = "gsk_YOUR_ACTUAL_KEY_HERE" 

def get_groq_response(system_prompt, user_prompt):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.5, 
            max_tokens=3000, # Increased for detailed answers
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_mock_test(subject, difficulty):
    # Dynamic Rules
    if difficulty == "Easy":
        marks = "2 Marks"
        depth = "Short Answer / Definition"
    elif difficulty == "Medium":
        marks = "5 Marks"
        depth = "Problem Solving / Derivation Steps"
    else: # Hard
        marks = "10 Marks"
        depth = "Complex GATE Level / Long Answer Proof"

    # Randomize Years to prevent repetition
    years = ["2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018"]
    random.shuffle(years)
    
    sys = "You are a Senior Professor & Exam Paper Setter for JNTUH University."
    
    prompt = f"""
    Create a {difficulty} Level Mock Test for the subject: {subject}.
    
    STRICT REQUIREMENTS:
    1. Generate EXACTLY 5 Multiple Choice Questions (MCQs).
    2. Difficulty: {marks} per question ({depth}).
    3. TAGS: Use these exact years for the 5 questions: [JNTUH R22 - {years[0]}], [JNTUH R18 - {years[1]}], [JNTUH R24 - {years[2]}], [JNTUH R18 - {years[3]}], [JNTUH R24 - {years[4]}].
    4. SUGGESTED ANSWER: For the 'Explanation', do NOT just say 'Option A is correct'. You MUST provide the full step-by-step calculation or theory that a student should write in the exam to get full marks.
    
    OUTPUT FORMAT (Do not deviate):
    
    ### Q1. [Question Text] [Tag]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    **Correct Answer:** [Option Letter]
    **Suggested Answer:** [Step-by-step detailed solution or derivation]
    
    (Repeat for Q2 to Q5)
    """
    return get_groq_response(sys, prompt)