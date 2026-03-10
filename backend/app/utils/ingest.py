from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

print("Loading the local 90MB embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Loading Ogaranya data...")
loader = TextLoader("data/formatted_knowledge_base.txt")
documents = loader.load()

print("Chopping data into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks of information.")

print("Translating text to numbers via API and saving to database...")
Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("\nSUCCESS! Your Ogaranya data is now embedded and saved in the 'chroma_db' folder.")