from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from schemas.chat import ChatState

class ConversationNode:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_template = PromptTemplate.from_template(
            """You are a friendly and helpful language tutor.
            The user said: {user_message}.

            Respond conversationally and helpfully. If you are unsure how to respond, you can suggest some things you are good at.
            For example: "That's a great question! I can help you with that. We could also work on something else, like you could ask me to 'generate a story' or we could do a 'grammar quiz'."
            """
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def __call__(self, state: ChatState) -> ChatState:
        response = self.chain.invoke({"user_message": state.user_message})
        state.tutor_response = response
        return state