import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain



def user_input(user_question):
     # Ensure conversational_chain is available
    if "conversational_chain" in st.session_state:
        response = st.session_state.conversational_chain({"question": user_question})
        st.session_state.chatHistory = response["chat_history"]

        for i, message in enumerate(st.session_state.chatHistory):
            if i % 2 == 0:
                st.write(f"User: {message['content']}")
            else:
                st.write(f"Bot: {message['content']}")
    else:
        st.warning("Please upload and process PDF documents before asking questions.")

def main():
    st.set_page_config("Information Retrieval System", layout="wide")
    st.header("Information Retrieval System")

     # Initialize session_state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if "conversational_chain" not in st.session_state:
        st.session_state.conversational_chain = None

    user_question = st.text_input("Ask a question for the PDF files:")

    if user_question:
        user_input(user_question)
    
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing documents..."):
                # Here you would add the logic to process the uploaded PDF documents
                raw_text = get_pdf_text(pdf_docs)
                print("Raw text type:", type(raw_text))
                print("Raw text content (preview):", str(raw_text)[:200])
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversational_chain = get_conversational_chain(vector_store)
                st.success("Done")
if __name__ == "__main__":
    main()

