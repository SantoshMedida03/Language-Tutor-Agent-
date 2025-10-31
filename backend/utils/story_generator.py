import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_story_content() -> str:
    """Generates a random short story using the LLM."""
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
    prompt_template = PromptTemplate.from_template(
        """Generate a random, simple, and engaging short story suitable for an English language learner.
        The story should be a few paragraphs long and introduce a few common vocabulary words naturally.
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({})
