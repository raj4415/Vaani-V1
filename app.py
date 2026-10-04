import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Vaani",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Vaani")
st.caption("A ChatGPT-style assistant powered by an OpenAI-compatible LLM API.")

# Read API key from Streamlit secrets.
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error(
        "OPENROUTER_API_KEY is not configured. "
        "Add it in Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# Conversation state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Vaani, a helpful, accurate and concise AI assistant. "
                "Answer in the user's language when possible. If you are uncertain, say so."
            ),
        }
    ]

# Sidebar
with st.sidebar:
    st.header("Settings")

    model = st.text_input(
        "Model",
        value="openrouter/free",
        help="openrouter/free automatically routes to an available free model.",
    )

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are Vaani, a helpful, accurate and concise AI assistant. "
                    "Answer in the user's language when possible. If you are uncertain, say so."
                ),
            }
        ]
        st.rerun()

    st.divider()
    st.caption("API key is stored in Streamlit Secrets and is not hard-coded in this app.")

# Display chat history, excluding system message.
for message in st.session_state.messages:
    if message["role"] in ("user", "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in stream:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                text = getattr(delta, "content", None)

                if text:
                    full_response += text
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as exc:
            error_message = (
                "Sorry, I couldn't get a response from the model.\n\n"
                f"**Error:** `{exc}`"
            )
            placeholder.error(error_message)
            # Keep the user message but don't add a failed assistant message.
