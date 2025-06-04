from commands.command import Command
from models.get_transcript import get_video_id, index_documents_to_chroma, get_vectorstore
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
            url_id = get_video_id(url)
            print(f"Successfully retrieved id: {url_id}")
            index_documents_to_chroma(url_id, self.session_id)
            print(f"Successfully indexed {url_id} in session {self.session_id}")


url = "https://www.youtube.com/watch?v=Bx4BYXOE9SQ"

session_id_number = "62f4fbcc-7e07-4c5e-ad00-032385725c64"
