import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_quiz_data(story_content: str) -> dict:
    """Generates a quiz JSON from a story using the LLM."""
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
    prompt_template = PromptTemplate.from_template(
        """
        You are a helpful assistant that generates quizzes.
        Based on the story below, generate a 5-question multiple-choice quiz to test comprehension.

        Story:
        {story}

        Return the quiz as a single, valid JSON object. Do NOT include any other text, explanations, or markdown formatting.
        The JSON object must have a "questions" key, which is a list of 5 question objects.
        Each question object must have: "question_text", "choices" (a list of 4 strings), and "correct_answer".
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    quiz_str = chain.invoke({"story": story_content})

    # Clean the output string
    if "```json" in quiz_str:
        quiz_str = quiz_str.split("```json")[1].strip()
    if "```" in quiz_str:
        quiz_str = quiz_str.split("```")[0].strip()
    
    try:
        return json.loads(quiz_str)
    except (json.JSONDecodeError, TypeError):
        return {}
