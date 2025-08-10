import PyPDF2
from sentence_transformers import SentenceTransformer
from backend.qdrant_client import get_qdrant_client
import uuid
import io
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def chunk_text(text, max_tokens=200):
    sentences = text.split(". ")
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_tokens:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "
    if current:
        chunks.append(current.strip())
    return chunks

def ingest_data(text, source, collection_name="docs"):
    chunks = chunk_text(text)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    client = get_qdrant_client(collection_name=collection_name)
    points = [
        {
            "id": str(uuid.uuid4()),
            "vector": embedding.tolist(),
            "payload": {"text": chunk, "source": source},
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=collection_name, points=points)
    return {"chunks_added": len(chunks)}

def ingest_pdf(filename, file_bytes, collection_name="docs"):
    pdf = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return ingest_data(text, filename, collection_name)

def ingest_youtube(youtube_url: str, collection_name: str = "docs"):
    transcript_text = ""
    try:
        # Extract video ID from the URL
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(youtube_url)
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
        elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        else:
            return {"error": "Invalid YouTube URL."}

        if not video_id:
            return {"error": "Could not extract video ID from YouTube URL."}


        
        try:
            # Try to get transcript in English or Hindi
            transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'hi'])
            transcript_text = " ".join([item.text for item in transcript_list])
            print(transcript_text)
        except NoTranscriptFound:
            logger.info(f"No transcript found for video ID: {video_id} in specified languages.")
            return {"error": "No transcript found for this video in English or Hindi."}
        except TranscriptsDisabled:
            logger.info(f"Transcripts are disabled for video ID: {video_id}.")
            return {"error": "Transcripts are disabled for this video."}
        except Exception as e:
            logger.error(f"Error retrieving YouTube transcript: {e}")
            return {"error": str(e)}

    except Exception as e:
        logger.error(f"Error processing YouTube URL: {e}")
        return {"error": str(e)}
    
    if transcript_text:
        return ingest_data(transcript_text, youtube_url, collection_name)
    else:
        return {"error": "Could not retrieve YouTube transcript."}
