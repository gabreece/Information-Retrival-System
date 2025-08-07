import streamlit as st


def main():
    st.set_page_config("Information Retrieval System", layout="wide")
    st.header("Information Retrieval System")
    
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing documents..."):
                # Here you would add the logic to process the uploaded PDF documents

                st.success("Done")
if __name__ == "__main__":
    main()

