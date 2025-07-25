import openai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # <-- .env dosyasını yükle

# Load API Key once
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def ask_llm(question, context=None, model="gpt-4o", system_prompt="You are a helpful business assistant."):
    """
    Sends a question to the LLM along with context and system prompt.
    Also stores the conversation in session_state using a session-based chat_key.
    Returns the assistant's reply.
    """

    # Prepare messages for the API
    messages = [{"role": "system", "content": system_prompt}]

    if context:
        messages.append({"role": "user", "content": f"Here is the product summary:\n{context}"})

    messages.append({"role": "user", "content": question})

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        reply = response.choices[0].message.content

        # Session-specific chat history key
        chat_key = f"chat_history_{st.session_state.session_id}"

        if chat_key not in st.session_state:
            st.session_state[chat_key] = []

        st.session_state[chat_key].extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": reply}
        ])

        return reply

    except Exception as e:
        return f"❌ LLM API error: {e}"



