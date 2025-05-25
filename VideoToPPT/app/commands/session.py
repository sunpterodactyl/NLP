from .command import Command
import uuid
import os 

class NewSessionCommand(Command):

    def execute(self):
        session_id=str(uuid.uuid4())
        session_path=os.path.join("sessions", session_id)
        os.makedirs(session_path, exist_ok=True)
        return  session_id, session_path
    