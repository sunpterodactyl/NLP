
'''
A class that generates a transcript document from each youtube video
Creates the document, chunks, and embedding in the chromadb
'''
from dotenv import load_dotenv
import os
import langchain 
import openai 

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langchain_core.documents import Document
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

#embedding and chunking capabilities
openai.api_key = os.getenv("OPENAI_API_KEY") 
embedding_function = OpenAIEmbeddings(openai_api_key = openai.api_key)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=60, length_function=len)

'''
Helper function to parse the url string and extract the video id
'''
def get_video_id(url: str) -> str:
    q = urlparse(url)
    if q.hostname == "youtu.be":
        return q.path[1:]
    elif q.hostname in ("www.youtube.com", "youtube.com"):
        if q.path == "/watch":
            return parse_qs(q.query)["v"][0]
    raise ValueError("Invalid YouTube URL")

'''

'''
def generate_document(video_id:str):
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)
    text = "\n".join([entry["text"] for entry in transcript_data])

    document = Document(
        page_content=text,
        metadata={"video_id": video_id}
    )
    return text_splitter.split_documents(document)


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
