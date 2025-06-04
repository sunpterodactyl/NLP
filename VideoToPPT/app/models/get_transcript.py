
'''
Indexes a transcript in chromadb but does not explicitly return a document
'''
from dotenv import load_dotenv
import os
import openai 
import re

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from exceptions.TranscriptException import TranscriptNotFoundError, TranscriptDisabledError


load_dotenv()

#embedding and chunking capabilities
openai.api_key = os.getenv("OPENAI_API_KEY") 
embedding_function = OpenAIEmbeddings(openai_api_key = openai.api_key)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60, length_function=len)

'''
Helper function to parse the url string and extract the video id
'''
def get_video_id(url):
    url_patterns = [
        r'v=([^&]+)',  # Pattern for URLs with 'v=' parameter
        r'youtu.be/([^?]+)',  # Pattern for shortened URLs
        r'youtube.com/embed/([^?]+)',# Pattern for embed URLs
        r'youtube\.com/watch\?v=([0-9A-Za-z_-]{11})',
    ]
    for pattern in url_patterns:
        match = re.search(pattern,url)
        if match:
            return match.group(1) #video_id
    
    raise ValueError("Incorrect url format. Please copy the format again")
    


def generate_document(video_id:str):

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)

        text = "\n".join([entry["text"] for entry in transcript_data])

        document = Document(
            page_content=text,
            metadata={"video_id": video_id}
        )
        return text_splitter.split_documents([document])
    except NoTranscriptFound:
        raise TranscriptNotFoundError(f"No transcript found in this video")
    except TranscriptDisabled:
        raise TranscriptDisabledError(f"Transcripts are not allowed to be used from this video. So sorry")
    except Exception as e:
        raise TranscriptNotFoundError(f'Error! {e}')


def index_documents_to_chroma(video_id: str, session_id) -> bool:
    vectorstore = get_vectorstore(session_id)
    try:
        doc_splits = generate_document(video_id)
        
        for split in doc_splits:
            split.metadata['video_id'] = video_id
        
        vectorstore.add_documents(doc_splits)
        return True 
    except Exception as e:
        print(f"Error: {e} while indexing youtube transcript for video: {video_id}")
        return False

def get_vectorstore(session_path: str):
    persist_dir = f"./ChromaDB/{session_path}"
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir, exist_ok=True)

    return Chroma(persist_directory=persist_dir, embedding_function=embedding_function)
