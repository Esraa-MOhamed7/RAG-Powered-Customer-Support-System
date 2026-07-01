from langchain_community.document_loaders import CSVLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1) Load Data
documents=[]

# 1.1 Policies
amazon_files=[
    "data/Amazon Refund Timelines - Amazon Customer Service.pdf",
    "data/Amazon Return Policy - Amazon Customer Service.pdf",
    "data/International Returns - Amazon Customer Service.pdf"
]

for file in amazon_files:
    loader=PyPDFLoader(file_path=file)
    pdf_docs=loader.load()
    for doc in pdf_docs:
        doc.metadata["source"] = "Amazon Official Policy"
    documents.extend(pdf_docs)

shopify_files = [
    "data/Shopify Help Center _ Returns and exchanges.pdf",
    "data/Shopify Help Center _ Creating and processing returns and exchanges.pdf",
    "data/Shopify Help Center _ Setting up return rules and return policy.pdf"
]

for file in shopify_files:
    loader=PyPDFLoader(file_path=file)
    pdf_docs=loader.load()
    for doc in pdf_docs:
        doc.metadata["source"]="Shopify Official Policy"
    documents.extend(pdf_docs)

# 1.2 CSV File
csv_path = "data/customer_support_tickets_new.csv"
csv_loader=CSVLoader(file_path=csv_path)
csv_docs=csv_loader.load()

for doc in csv_docs:
    doc.metadata["source"]="Historical Support Tickets"
    documents.append(doc)

print(f"Total Documents: {len(documents)}")

# 2) Data Splitting
r_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n","\n"," ",""]
)

splitts=r_splitter.split_documents(documents)
print(len(splitts))

# 3) Embeddings
embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# 4) Save vectores in data base
persist_directory="./chroma_db"
vectore_db=Chroma.from_documents(
    documents=splitts,
    embedding=embeddings,
    persist_directory=persist_directory
)

print("Pipline finished successfully")