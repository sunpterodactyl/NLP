from ..models.get_transcript import get_vectorstore
from ..commands.command import Command
from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from ..schemas.pydantic_models import QueryResponse, QueryInput
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pptx import Presentation

import requests
from dotenv import load_dotenv
import os

load_dotenv()

access_id = os.getenv("MAGICSLIDES_ID")
SESSION = "5aada9c7-05a4-4f6e-aa74-5ae4bb688178" #remove after testing this out locally

class GeneratePPT(Command):

    def __init__(self, input:QueryInput):
        self.session_id = input.session_id
        self.model_name = input.model
        self.query = input.query

    def execute(self):
        vectorstore = get_vectorstore(self.session_id)
        qa_response = run_langchain_qa_chain(vectorstore, self.query, self.model_name, self.session_id)

        prs = Presentation()
        #TODO change the API here and use python pptx instead 
        '''
        try:
            req = requests.post(
                'https://api.magicslides.app/public/api/ppt_from_summery',
                json={
                    'msSummaryText': qa_response.response,
                    'email': 'inforsunpteranadon@gmail.com',       
                    'accessId': access_id,               
                    'template': 'bullet-point1',
                    'language': 'en',
                    'slideCount': 10,
                    'aiImages': False,
                    'imageForEachSlide': True,
                    'googleImage': False,
                    'googleText': False,
                    'model': self.model_name,
                    'presentationFor': qa_response.audience
                }
            )
            req.raise_for_status()
            ppt_url = req.json().get('url')
            return ppt_url
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to generate PPT: {e}")
        '''



def run_langchain_qa_chain(vectorstore, prompt: str, model_name: str, session_id:str) -> QueryResponse:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=model_name)

    prompt_template = ChatPromptTemplate.from_template(
    """Generate a deep answer, structure in the form of slides to the question based on the following context:

    Context: {context}

    Question: {question}

        Answer: Respond with structure such as Slide 1:, Slide 2:, Slide 3: and so on."""
)
    qa_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        |prompt_template
        |llm
        |StrOutputParser()
    )

    response = qa_chain.invoke(prompt)
    print(f"Response generated")

    audience_prompt = ChatPromptTemplate.from_template("""
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
    
    audience_chain = audience_prompt | llm |StrOutputParser()
    audience = audience_chain.invoke({"content": response}).strip()
    print(f"QueryResponse Object Generating")

    return QueryResponse (
        response = response,
        audience = audience,
        session_id=session_id,
        model=model_name
        )
    

q = QueryInput(
    query = "How can I use hugging face as an AI engineer and why should I use it",
    session_id=SESSION
)

cmd = GeneratePPT(q)
print(cmd.execute())
