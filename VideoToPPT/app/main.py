
from fastapi import FastAPI, HTTPException
from schemas.pydantic_models import QueryInput, QueryResponse, IndexInput
from commands.save_url import IndexCommand
from commands.generate_ppt import GeneratePPT
from commands.session import NewSessionCommand

import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
app=FastAPI()


#prompt
@app.post("/ppt")
def get_ppt(query: QueryInput):
    command = GeneratePPT(query)
    result = command.execute(
        prompt=input.prompt,
        session_id=input.session_id,
        model_name=input.model
    )
    return result


#session
'''
When clicked a new session id is generated
'''
@app.get("/session")
def get_new_session():
    command = NewSessionCommand()
    return command.execute()


#url 
@app.post("/index")
def index(q: IndexInput):
    urls = input.urls if isinstance(input.urls, list) else [input.urls]
    command = IndexCommand(urls=urls, session_id=input.session_id)
    command.execute()
    return {"message": "Documents indexed successfully", "session_id": input.session_id}

