import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(
        persist_directory="chroma_store",
        anonymized_telemetry=False
    )
)

conversation_collection = client.get_or_create_collection(
    name="sales_conversations"
)
