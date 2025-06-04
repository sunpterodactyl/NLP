from commands.command import Command
import uuid
import os 

'''
Deletes all existing documents from the ChromaDB
'''
class NewSessionCommand(Command):

    def execute(self) -> str:
        session_id=str(uuid.uuid4())
        session_path=os.path.join("sessions", session_id)
        os.makedirs(session_path)
        return session_id
    