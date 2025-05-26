from ..commands.command import Command
from ..models.get_transcript import get_video_id, index_documents_to_chroma, get_vectorstore
from typing import Union, List


class IndexCommand(Command):

    def __init__(self, urls: Union[str, List[str]], session_id:str):
        self.urls = urls
        self.session_id = session_id

    def execute(self):
        vectorstore = get_vectorstore(session_path=self.session_id)
        if isinstance(self.urls, str):
            self.urls = [self.urls]
        else:
            pass
        
        for url in self.urls:
            id = get_video_id(url)
            print(f"Successfully retrieved id: {id}")
            index_documents_to_chroma(id, self.session_id)
            print(f"Successfully indexed {id} in session {self.session_id}")

SESSION = "5aada9c7-05a4-4f6e-aa74-5ae4bb688178"
URL = "https://www.youtube.com/watch?v=3kRB2TXewus"
curr = IndexCommand(URL, SESSION)
print(curr.execute())

