import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


print("Waking up the local database...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Retrieving the top 3 most relevant chunks of info when asked a question
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("Connecting to the AI Brain...")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2, api_key=GROQ_API_KEY)

system_prompt = (
    "You are a helpful, polite, and professional customer support assistant for Ogaranya. "
    "Ogaranya is an Offline-to-Online (O2O) convenience commerce platform. "
    "Use ONLY the provided context to answer the user's question. "
    "Always include the necessary SMS commands and phone numbers if they are in the context. "
    "If the answer is not in the context, say 'I am sorry, but I don't have that information. Let me connect you to a human agent.' "
    "Do NOT make up answers or use outside knowledge. \n\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print("\n" + "=" * 50)
print("🤖 Ogaranya Support Bot is online! Type 'quit' to exit.")
print("=" * 50)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ['quit', 'exit', 'q']:
        print("\nBot: Goodbye! Have a great day.")
        break

    response = rag_chain.invoke({"input": user_input})
    print(f"\nBot: {response['answer']}")