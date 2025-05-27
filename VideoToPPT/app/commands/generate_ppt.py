from ..models.get_transcript import get_vectorstore
from ..commands.command import Command
from langchain_openai.chat_models import ChatOpenAI
from ..schemas.pydantic_models import QueryResponse, QueryInput, SlideResponse
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pptx import Presentation

from dotenv import load_dotenv
import os

load_dotenv()

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
       



def run_langchain_qa_chain(vectorstore, prompt: str, model_name: str, session_id:str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=model_name)

    parser = PydanticOutputParser(pydantic_object=SlideResponse)
    format_instructions = parser.get_format_instructions()
    print(format_instructions)

    PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
    """Generate a comprehensive presentation based on the following context and question.
        Create exactly 10 slides that thoroughly cover the topic.

        Context: {context}

        Question: {question}

        {format_instructions}

        Generate slides that cover the topic comprehensively. Each slide should have:
        - A clear, descriptive title
        - 3-5 bullet points with key information
        - Detailed slide content that expands on the bullet points
        - A boolean indicating if an image would enhance understanding

        Response:"""
    )

    qa_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
            "format_instructions": lambda _: format_instructions
        }
        | PROMPT_TEMPLATE
        | llm
        | parser
    )



    try: 
        response = qa_chain.invoke(prompt) 
        print(response)
        print(f"Generated {len(response.content)} slides")

        
        for i, slide in enumerate(response.content, 1):
           print(f"Slide {i}: {slide.title}")
           print(f"Bullet points: {slide.bullet_points}")
           print(f"Needs image: {slide.image}")

        return QueryResponse (
            response = response,
            session_id=session_id,
            model=model_name
        )
        
    except Exception as e:
        print(f"Raised exception {e}")
        return None

    

q = QueryInput(
    query = "How can I use hugging face as an AI engineer and why should I use it",
    session_id=SESSION
)

cmd = GeneratePPT(q)
print(cmd.execute())
