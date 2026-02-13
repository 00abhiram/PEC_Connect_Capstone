import google.generativeai as genai
import streamlit as st

# 1. Load the key directly from the secrets file
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    print(f"✅ Found API Key: {api_key[:5]}...{api_key[-5:]}") # Prints first/last 5 chars
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"❌ Error loading Key: {e}")
    exit()

# 2. Ask Google which models are available
print("\n🔍 Checking available models...")
try:
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   - Available: {m.name}")
            found_any = True
            
    if not found_any:
        print("❌ Connects to Google, but NO models found. (Check if Generative Language API is enabled in Google Console)")
    else:
        print("\n✅ SUCCESS! Your API Key works.")
        
except Exception as e:
    print(f"\n❌ FATAL ERROR: Your API Key is invalid or blocked.\nError details: {e}")