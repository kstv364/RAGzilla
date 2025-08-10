from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

_qdrant_clients = {}

import os # Added os import
def get_qdrant_client(collection_name: str = "docs"):
    if collection_name not in _qdrant_clients:
        logger.info(f"Initializing Qdrant client for collection: {collection_name}")
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
        client = QdrantClient(host=qdrant_host, port=qdrant_port)
        
        # Check if collection exists, if not, create it
        collections = client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            logger.info(f"Collection '{collection_name}' not found. Creating it.")
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            logger.info(f"Collection '{collection_name}' created.")
        else:
            logger.info(f"Collection '{collection_name}' already exists. Reusing it.")
        _qdrant_clients[collection_name] = client
    return _qdrant_clients[collection_name]
