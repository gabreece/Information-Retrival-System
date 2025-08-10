import os 
import sys
import asyncio
import google.generativeai as palm
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.chains import conversational_retrieval
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv




load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    text_chunks = text_splitter.split_text(text)
    return text_chunks

def get_vector_store(text_chunks):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


    embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversational_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversational_chain


