import os
import datetime
from dotenv import load_dotenv
import streamlit as st

# Modern stable imports for 2026
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="AI Agent Workshop", page_icon="🤖")
st.title("🤖 Modern Gemini Agent")
st.caption("Built with LangChain v1.0 & Gemini 3.1 Flash")
st.radio("Choose an option:", ["easy", "medium", "hard"])
st.menu_button("Options", ["Clear Chat", "Reset Agent"])
st.file_uploader("Upload a file to analyze...")

# 1. Define the Tool (The "Hands")
@tool
def get_system_time(query: str) -> str:
    """Returns the current system time. Use this for questions about 'now' or 'time'."""
    # Logic: Tools should return strings for the LLM to parse easily
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The current system time is {now}."

# 2. Setup the Brain
# Using Gemini 3.1 Flash/Flash-Lite for high-speed tool calling
llm = ChatGoogleGenerativeAI(model="gemini-3.1-Flash", temperature=0)

# 3. Assemble the Agent
tools = [get_system_time]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant. Give me solid examples and responses."
)

# --- Streamlit Chat UI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! Ask me anything about the current time."})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Loop
if prompt := st.chat_input("Ask me the time..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response Logic
    with st.chat_message("assistant"):
        # We use st.status to show the "Thought" process to the students
        with st.status("Agent is thinking...", expanded=True) as status:
            inputs = {"messages": [("user", prompt)]}
            try:
                response = agent.invoke(inputs)
                final_text = response["messages"][-1].content
                status.update(label="Logic complete!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Error occurred", state="error")
                final_text = f"I encountered an error: {str(e)}"

        st.markdown(final_text)
        st.session_state.messages.append({"role": "assistant", "content": final_text})
        st.success("Response generated!")
        st.balloons()
        st.write("Feel free to ask another question or try out the other options!")
        st.write("---")
        st.write("This is a demo of a modern AI agent using Gemini 3.1 Flash and LangChain v1.0. The agent can call tools to get real-time information, like the current system time. Try asking it about the time or explore the other options in the menu!")  