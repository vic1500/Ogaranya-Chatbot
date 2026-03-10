from langchain_huggingface import HuggingFaceEmbeddings

class ModelRegistry:
    embeddings_model = None

model = ModelRegistry()

def load_models():
    print("🔃 Loading Embedding model....")
    model.embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("✅ Embedding model loaded.")