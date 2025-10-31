from langgraph.graph import StateGraph, END
from langgraph.nodes import ConversationNode, StoryGenerationNode, QuizNode
from .nodes.router import RouterNode
from .nodes.grammar_quiz import GrammarQuizNode
from .nodes.vocabulary_quiz import VocabularyQuizNode
from schemas.chat import ChatState

# A simple node that does nothing, used to terminate a graph path.
def end_conversation(state: ChatState) -> ChatState:
    return state

def create_graph():
    graph = StateGraph(ChatState)

    graph.add_node("router", RouterNode())
    graph.add_node("conversation", ConversationNode())
    graph.add_node("story", StoryGenerationNode())
    graph.add_node("quiz", QuizNode())
    graph.add_node("grammar_quiz", GrammarQuizNode())
    graph.add_node("vocabulary_quiz", VocabularyQuizNode())
    graph.add_node("end_conversation", end_conversation)

    graph.set_entry_point("router")

    # The router decides the path.
    graph.add_conditional_edges(
        "router",
        lambda state: state.next_node,
        {
            "story": "story",
            "quiz": "quiz",
            "grammar_quiz": "grammar_quiz",
            "vocabulary_quiz": "vocabulary_quiz",
            "conversation": "conversation",
            "end_conversation": "end_conversation"
        }
    )

    # All paths end after their primary action.
    graph.add_edge("conversation", END)
    graph.add_edge("story", END)
    graph.add_edge("quiz", END)
    graph.add_edge("grammar_quiz", END)
    graph.add_edge("vocabulary_quiz", END)
    graph.add_edge("end_conversation", END)

    return graph.compile()