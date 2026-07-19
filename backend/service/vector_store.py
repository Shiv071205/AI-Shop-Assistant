import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()  # Load environment variables from .env file

#init embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

#init pinecone client
pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("shop-assistant")

#vector store
VectorStore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="Description"
    
)



