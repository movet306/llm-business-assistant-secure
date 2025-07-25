# --- llm_dashboard.py ---

import streamlit as st
import pandas as pd
import uuid
from product_analysis import clean_product_data, generate_llm_context
from llm_agent import ask_llm
from fpdf import FPDF

# --- Load default data ---
def load_default_data():
    try:
        df = pd.read_json("products.json")
        df = clean_product_data(df)
        return df
    except Exception as e:
        st.error(f"❌ Failed to load default data: {e}")
        return pd.DataFrame()

# --- Session: Load if not yet ---
if "context" not in st.session_state or "df" not in st.session_state:
    df = load_default_data()
    context = generate_llm_context(df)
    st.session_state["df"] = df
    st.session_state["context"] = context

# --- Sidebar: Admin Panel ---
st.sidebar.header("⚙️ Admin Panel")
uploaded_file = st.sidebar.file_uploader("📂 Upload Your Product Data", type=["csv", "json", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        df = clean_product_data(df)
        context = generate_llm_context(df)

        st.session_state["context"] = context
        st.session_state["df"] = df
        st.sidebar.success("✅ Custom data uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to read uploaded file: {e}")

# --- Session ID for chat history ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
chat_key = f"chat_history_{st.session_state.session_id}"
if chat_key not in st.session_state:
    st.session_state[chat_key] = []

# --- Defaults ---
if "context" not in st.session_state:
    st.session_state["context"] = ""
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()

# --- Reload default data ---
if st.sidebar.button("🔄 Reload Product Data"):
    df = load_default_data()
    context = generate_llm_context(df)
    st.session_state["context"] = context
    st.session_state["df"] = df

# --- Sidebar: LLM Settings ---
st.session_state.system_prompt = st.sidebar.text_area(
    "🧠 Set Custom System Prompt", value="You are a helpful business assistant.", height=100)
st.session_state.model_choice = st.sidebar.selectbox("🤖 Select LLM Model", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"])

# --- UI ---
st.set_page_config(page_title="LLM Business Assistant", layout="centered")
st.title("🧠 LLM Business Assistant")
st.markdown("Ask questions about your product dataset, and let the AI assistant help you make better decisions.")
st.markdown(
    """
    <div style='margin-top: -5px; text-align: center; color: #666666; font-size: 16px; font-style: italic;'>
        <span style='font-weight: 500;'>Builty by</span> <span style='font-weight: 600;'>Mert Ovet</span>
    </div>
    """,
    unsafe_allow_html=True
)
# --- Suggested Questions ---
st.subheader("🔍 Suggested Insights")
suggested_questions = [
    "Which product category is the most expensive?",
    "Which category has the highest customer satisfaction?",
    "Which price segment has the most products?",
]
for q in suggested_questions:
    with st.expander(f"💡 {q}"):
        try:
            response = ask_llm(
                q,
                st.session_state["context"],
                model=st.session_state.model_choice,
                system_prompt=st.session_state.system_prompt
            )
            st.markdown(response)
        except Exception as e:
            st.error(f"LLM error: {e}")

# --- Context Viewer ---
with st.expander("📊 Product Summary (used as context)", expanded=False):
    st.text(st.session_state["context"])

# --- User Question ---
user_question = st.text_input("💬 Enter your business question", placeholder="e.g., Which category has the highest customer satisfaction?")
if st.button("Ask LLM") and user_question:
    with st.spinner("Thinking..."):
        response = ask_llm(
            user_question,
            st.session_state["context"],
            model=st.session_state.model_choice,
            system_prompt=st.session_state.system_prompt
        )
        st.success("✅ LLM Response")
        st.markdown(response)
        st.session_state[chat_key].append({"role": "user", "content": user_question})
        st.session_state[chat_key].append({"role": "assistant", "content": response})

# --- Chat History ---
if st.session_state.get(chat_key):
    st.subheader("🔈 Chat History")
    for msg in st.session_state[chat_key]:
        role = "🧑‍💼 You" if msg["role"] == "user" else "🧠 Assistant"
        st.markdown(f"**{role}:** {msg['content']}")

    chat_df = pd.DataFrame(st.session_state[chat_key])
    st.download_button("📅 Download Chat History (CSV)", chat_df.to_csv(index=False), "chat_history.csv")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="LLM Business Assistant - Chat History\n")
    pdf.ln()
    for msg in st.session_state[chat_key]:
        role = msg["role"].capitalize()
        pdf.multi_cell(0, 10, txt=f"{role}: {msg['content']}\n")
        pdf.ln()
    pdf_output = pdf.output(dest='S').encode('utf-8')
st.download_button("📄 Download Chat History (PDF)", pdf_output, "chat_history.pdf", mime="application/pdf")



