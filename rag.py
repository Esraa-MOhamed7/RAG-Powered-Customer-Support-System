from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# 0) SECRETS
load_dotenv("secret.env")

# 1) Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2) Read data from vector database
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
print(f"Total documents in DB: {db._collection.count()}")

# 3) Use MMR
mmr_retriever = db.as_retriever(search_type='mmr', search_kwargs={"k": 3})

# 4) Define the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just reformulate it if needed."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

context_chain = contextualize_q_prompt | llm | StrOutputParser()


# 5) Customize a Prompt 
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an elite customer support assistant. Answer the user's question strictly based ONLY on the provided context.

Instructions:
1. If the context does not contain the answer, reply exactly with: "I am sorry, but I cannot find the answer to this in the official policies or historical tickets." Do not invent facts.
2. If the answer is found, cite the source at the very beginning of your answer:
   - For Amazon policies, use "[Source: Amazon Official Policy]"
   - For Shopify policies, use "[Source: Shopify Official Policy]"
   - For support tickets, use "[Source: Historical Support Tickets]"

Context:
{context}"""),
    
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# 6) LCEL 
def format_docs(docs):
    if not docs:
        print("  Warning: Retriever returned ZERO documents!")
    for doc in docs:
        print(f" Retrieved Chunk Source: {doc.metadata.get('source')}") 
    return "\n\n".join(doc.page_content for doc in docs)

def custom_rag_logic(input_data):
    if input_data.get("chat_history"):
        smart_question = context_chain.invoke({
            "chat_history": input_data["chat_history"],
            "question": input_data["question"]
        })
        print(f" [Smart Reformulation]: {smart_question}")
    else:
        smart_question = input_data["question"]
    
    docs = mmr_retriever.invoke(smart_question)
    context = format_docs(docs)
    
    return (qa_prompt | llm | StrOutputParser()).invoke({
        "context": context,
        "chat_history": input_data["chat_history"],
        "question": input_data["question"]
    })

rag_chain = custom_rag_logic

# 7) Lets Test
if __name__ == "__main__":
    history = [] 
    print("\n Running Absolute RAG Test with Smart Memory...")
    
    query1 = "How can I issue a refund on Shopify?"
    response1 = rag_chain({"question": query1, "chat_history": history})
    print(f"\nUser: {query1}\nAI: {response1}\n")
    
    history.append(("human", query1))
    history.append(("ai", response1))
    
    query2 = "Does it take a long time?"
    response2 = rag_chain({"question": query2, "chat_history": history})
    print(f"\nUser: {query2}\nAI: {response2}\n")