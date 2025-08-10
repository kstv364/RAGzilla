from sentence_transformers import SentenceTransformer
from backend.qdrant_client import get_qdrant_client
from backend.llm_client import generate_answer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def answer_query(query: str, collection_name: str = "docs"):
    logger.info(f"Answering query: '{query}' from collection: '{collection_name}'")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    q_vector = embedder.encode([query])[0].tolist()
    client = get_qdrant_client(collection_name=collection_name)
    hits = client.search(
        collection_name=collection_name, query_vector=q_vector, limit=5
    )
    context = "\n".join([hit.payload["text"] for hit in hits])
    logger.info(f"Retrieved context: {context[:200]}...") # Log first 200 chars of context
    return generate_answer(query, context)
