from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,OpenAI
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

if __name__=="__main__":
    pdf_path = "fnins-14-579365.pdf"
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100,chunk_overlap=0,separator="\n")
    docs = text_splitter.split_documents(documents=documents)
    print(len(docs))

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs,embeddings)
    vectorstore.save_local("faiss_index_test")

    new_vectorstore = FAISS.load_local("faiss_index_test",embeddings,allow_dangerous_deserialization=True)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        OpenAI(),retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(new_vectorstore.as_retriever(),combine_docs_chain)

    res = retrieval_chain.invoke({"input":"Give me the gist of osteopathy in 3 sentences"})

    print(res["answer"])
