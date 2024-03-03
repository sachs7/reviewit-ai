import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.chains import LLMChain

from system_message import system_template

# Initialize chat history from session state (if available)
chat_history = st.session_state.get("chat_history", [])

# Create the LLM and prompt templates
llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

user_template = HumanMessagePromptTemplate.from_template("{user_prompt}")
template = ChatPromptTemplate.from_messages([system_template, user_template])
chain = LLMChain(llm=llm, prompt=template)


def get_code_review(user_prompt):
    """Retrieves a code review from the LLM based on the user's prompt."""
    return chain.invoke({"user_prompt": user_prompt}).get(
        "text", "No review available."
    )


# Define the Streamlit app and set full-width layout
st.set_page_config(layout="wide")
st.title("ReviewIt AI")

# Create two containers with spacing
col1, col2 = st.columns([5, 2])  # Adjust column widths as needed

with col1:
    # Prompt and response section
    user_code = st.text_area("Enter your code to be reviewed")

    if st.button("Get Code Review"):
        with st.spinner("Generating review..."):
            review = get_code_review(user_code)
            chat_history.append({"user_prompt": user_code, "review": review})
            st.session_state.chat_history = chat_history

        st.write("Review:", review)

with col2:
    # Chat history section
    if chat_history:
        st.subheader("Chat History:")
        # Reverse the chat history list before iterating
        for interaction in chat_history[::-1]:
            st.markdown(f"**User:** {interaction['user_prompt']}")
            st.markdown(f"**Review:** {interaction['review']}")
            st.markdown("---")
    else:
        st.write("No previous interactions.")
