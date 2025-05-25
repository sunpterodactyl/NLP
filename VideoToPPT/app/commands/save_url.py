from .command import Command
from models.get_transcript import get_video_id, index_documents_to_chroma, get_vectorstore
from typing import Union, List


class IndexCommand(Command):

    def __init__(self, urls: Union[str, List[str]], session_id:str):
        self.urls = urls
        self.session_id = session_id

    def execute(self):
        vectorstore = get_vectorstore(session_path=self.session_id)

        for url in self.urls:
            id = get_video_id(url)
            index_documents_to_chroma(id, self.session_id)
