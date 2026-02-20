import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
print("API key present?", bool(API_KEY))
if API_KEY:
    genai.configure(api_key=API_KEY)
    models = genai.list_models()
    for m in models:
        # Print the object for inspection
        print(repr(m))
else:
    print("No API key loaded.")
