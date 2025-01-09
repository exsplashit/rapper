import streamlit as st
from rag.retriever import Retriever
from rag.generator import Generator
from rag.agent import Agent

# Initialize components
retriever = Retriever()
generator = Generator()
agent = Agent(retriever, generator)

st.title("RAG-based Question Answering")
st.markdown("Ask questions based on the scraped song lyrics.")

query = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if query:
        with st.spinner("Retrieving and generating answer..."):
            try:
                answer = agent.answer(query)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question.")
