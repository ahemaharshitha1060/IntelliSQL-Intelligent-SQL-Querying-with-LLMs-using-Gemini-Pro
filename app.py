import os
import streamlit as st
import sqlite3
from dotenv import load_dotenv

# generative AI client from Google
from google import generativeai as genai

# load environment variables from .env file
load_dotenv()

# configure the Google generative AI client
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
else:
    genai.configure(api_key=API_KEY)


# prompt design for converting english questions to SQL queries
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


def get_response(que: str, prompt_list: list) -> str:
    """Ask the Gemini model to convert a natural language query into SQL."""
    # use a model name that exists for the v1beta endpoint; list_models() output
    # shows several options such as "gemini-2.5-pro" or "gemini-pro-latest".
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content([prompt_list[0], que])
    return response.text


def read_query(sql: str, db: str = "data.db"):
    """Execute the provided SQL on the provided SQLite database and return the rows."""
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        conn.commit()
        conn.close()
    return rows


# ---------- page renderers ----------

def page_home():
    st.markdown(
        """
        <style>
        body { background-color: #2E2E2E; }
        .title { color: green; text-align:center; }
        .subtitle { color: green; text-align:center; }
        .offerings { color: white; font-size: 1.1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 class='title'>Welcome to IntelliSQL!</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h3 class='subtitle'>Revolutionizing Database Querying with Advanced LLM Capabilities</h3>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://img.icons8.com/color/96/000000/data-warehouse.png")
    with col2:
        st.markdown(
            "<div class='offerings'>"
            "<ul>"
            "<li>Intelligent query assistance and syntax suggestions</li>"
            "<li>Natural‑language‑to‑SQL translation</li>"
            "<li>Efficient data retrieval and performance tips</li>"
            "<li>Data exploration & trend analysis</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )


def page_about():
    st.markdown(
        """
        <style>
        .content { color: white; }
        .title { color: green; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 class='title'>About IntelliSQL</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='content'>
        IntelliSQL is a proof-of-concept application that leverages
        advanced large language models to make SQL querying accessible
        to users of all skill levels.  By translating natural language
        questions into executable SQL and returning results from a
        SQLite back end, the platform enables intuitive data exploration
        and intelligent query assistance.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/97/Oracle_SQL_Developer_logo.png")


def page_intelligent_query_assistance():
    st.markdown(
        """
        <style>
        .tool-input { margin-top: 1rem; color:white; }
        .response { margin-top: 1rem; color:white; }
        .title { color: green; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 class='title'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)
    st.write(
        "Enter a natural language question and the system will generate an SQL statement",
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("Ask your question", "How many students are in the database?")
        if st.button("Convert & Run") or query:
            try:
                sql_query = get_response(query, prompt)
                st.markdown(f"**Generated SQL:** `{sql_query}`")
                results = read_query(sql_query)
                if results:
                    st.write(results)
                else:
                    st.write("(no rows returned)")
            except Exception as exc:
                st.error(f"Error: {exc}")
    with col2:
        st.image("https://img.icons8.com/color/96/000000/query.png")


def main():
    st.set_page_config(page_title="IntelliSQL", page_icon="⭐", layout="wide")
    st.sidebar.title("Navigation")
    st.sidebar.markdown(
        "<style> .sidebar .sidebar-content { background-color: #2E2E2E; color: white; } </style>",
        unsafe_allow_html=True,
    )

    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
    }
    choice = st.sidebar.radio("Go to", list(pages.keys()))
    pages[choice]()


if __name__ == "__main__":
    main()
