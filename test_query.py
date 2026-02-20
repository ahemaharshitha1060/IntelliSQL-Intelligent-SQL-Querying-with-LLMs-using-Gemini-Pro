import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing API key")
genai.configure(api_key=API_KEY)

prompt = [
    (
        "You are an expert in converting English questions to SQL queries.\n"
        "The database is named STUDENTS and has the following columns: NAME, CLASS, Marks, Company.\n"
        "Examples:\n"
        "Question: How many entries of records are present?\n"
        "SQL: SELECT COUNT(*) FROM STUDENTS;\n"
        "Question: Tell me all the students studying in MCom class?\n"
        "SQL: SELECT * FROM STUDENTS WHERE CLASS=\"MCom\";"
    )
]

model = genai.GenerativeModel("gemini-2.5-pro")
response = model.generate_content([prompt[0], "How many students are in the database?"])
print("response text:\n", response.text)
