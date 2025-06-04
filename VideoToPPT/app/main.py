import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas.pydantic_models import QueryInput, IndexInput
from commands.save_url import IndexCommand
from commands.generate_ppt import GeneratePPT
from commands.session import NewSessionCommand
from exceptions.TranscriptException import TranscriptNotFoundError, TranscriptDisabledError

import logging
import os

logging.basicConfig(filename='app.log', level=logging.INFO)
app=FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "ok", "message": "PPT Generator API is running"}

#prompt
@app.post("/ppt")
def get_ppt(query: QueryInput):
    """Return a PPT for the given prompt"""
    command = GeneratePPT(query)
    filepath = command.execute() #rmove this capability
    try:
        os.makedirs('presentations', exist_ok=True)
        UPLOAD_PATH = os.path.join('presentations', f'{query.session_id}.pptx')
        return FileResponse(
            path=UPLOAD_PATH,
            filename=f'{query.session_id}.pptx',
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e}: Failed to generate presentation')


#session

@app.get("/session")
def get_new_session():
    try:
        command = NewSessionCommand()
        return command.execute()
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create a new session {str(e)}"
        )


#url 
@app.post("/index")
def index(input: IndexInput):
    urls = input.urls if isinstance(input.urls, list) else [input.urls]

    if not input.session_id:
        input.session_id = NewSessionCommand().execute() #create a new session id

    command = IndexCommand(urls=urls, session_id=input.session_id)
    try:
        command.execute()
        return {"message": "Documents indexed successfully", "session_id": input.session_id}
    except TranscriptNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail= "Error finding transcript for this link"
        )
    except TranscriptDisabledError as e:
        raise HTTPException(
            status_code=403,
            detail="Transcripts are not allowed for this video :/"
        )

'''
Note that index should take in multiple urls and index them according to the index command
Also note that both the database and the query_input should be aware of the session_id
can there be multiple users and what happens to the session then
'''


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
