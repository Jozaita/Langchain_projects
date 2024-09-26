import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


if __name__ == "__main__":
    print("Loading document...")
    loader = TextLoader("mediumblog1.txt")
    document = loader.load()
    print("Splitting document...")
    text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
    print("Ingesting embeddings...")
    PineconeVectorStore.from_documents(texts,embeddings,index_name=os.environ.get('INDEX_NAME'))
    print("Finished")
    
