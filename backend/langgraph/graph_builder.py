from langgraph.graph import StateGraph, END
from langgraph.nodes import ConversationNode, VocabularyNode, StoryGenerationNode, QuizNode, AdaptationNode
from schemas.chat import ChatState

def create_graph():
    graph = StateGraph(ChatState)

    graph.add_node("conversation", ConversationNode())
    graph.add_node("vocabulary", VocabularyNode())
    graph.add_node("story", StoryGenerationNode())
    graph.add_node("quiz", QuizNode())
    graph.add_node("adaptation", AdaptationNode())

    graph.set_entry_point("conversation")

    graph.add_edge("conversation", "vocabulary")
    graph.add_edge("vocabulary", "story")
    graph.add_edge("story", "quiz")
    graph.add_edge("quiz", "adaptation")
    graph.add_edge("adaptation", END)

    return graph.compile()