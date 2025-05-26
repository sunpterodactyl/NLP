from models.get_transcript import get_vectorstore
from command import Command
from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from schemas.pydantic_models import QueryResponse, QueryInput

import requests
from dotenv import load_dotenv
import os

load_dotenv() 

access_id = os.getenv("MAGICSLIDES_ID")

class GeneratePPT(Command):

    def __init__(self, input:QueryInput):
        self.session_id = input.session_id
        self.model_name = input.model
        self.query = input.query

    def execute(self):
        vectorstore = get_vectorstore(self.session_id)
        response = run_langchain_qa_chain(vectorstore, self.query, self.model_name, self.session_id)

        try:
            response = requests.post(
                'https://api.magicslides.app/public/api/ppt_from_summery',
                json={
                    'msSummaryText': response.response,
                    'email': 'inforsunpteranadon@gmail.com',       
                    'accessId': access_id,               
                    'template': 'bullet-point1',
                    'language': 'en',
                    'slideCount': 10,
                    'aiImages': False,
                    'imageForEachSlide': True,
                    'googleImage': False,
                    'googleText': False,
                    'model': self.model.value,
                    'presentationFor': response.audience
                }
            )
            response.raise_for_status()
            ppt_url = response.json().get('url')
            return ppt_url
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate PPT: {e}")




def run_langchain_qa_chain(vectorstore, prompt: str, model_name: str, session_id:str) -> QueryResponse:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=model_name)
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = chain.run(prompt)

    audience_prompt = PromptTemplate.from_template("""
    Given the following content, determine the most appropriate audience.
    Respond with a short phrase such as:
    - high school students
    - university students
    - general public
    - researchers
    - business professionals
    - domain experts

    Content:
    {content}
    """)
    
    audience_chain = LLMChain(llm=llm, prompt=audience_prompt)
    audience = audience_chain.run(content=response).strip()

    return QueryResponse (
        response = response,
        audience = audience,
        session_id=session_id,
        model=model_name
        )

