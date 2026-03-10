import os

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from app.schemas.chat import UserInput
from app.ml.load_model import model

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

chat_router = APIRouter()

vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=model.embeddings_model)

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

@chat_router.post("/chat")
async def response(data: UserInput):
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    user_input = data.input_text

    if not user_input or not user_input.strip():
        raise HTTPException(400, "Message cannot be empty.")

    try:
        response = await rag_chain.ainvoke({"input": user_input})
        return {"reply": response["answer"]}
    except Exception as e:
        raise HTTPException(500, f"An error occurred while processing your request - {str(e)}")

