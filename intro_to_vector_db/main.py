import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

if __name__ == '__main__':

    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    query = "What is pinecone in machine learning ? "
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    print(result.content)

    vectorstore = PineconeVectorStore(
        index_name=os.environ.get('INDEX_NAME'),
        embedding=embeddings
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm,retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=combine_docs_chain
    )


    template  = """ Use the following pieces of context to answer the question at  the end. 
    If you do not know the answer, just say you do not know, do not try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible. 

    {context}

    Question: {question}

    Helpful answer: """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context":vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
    )