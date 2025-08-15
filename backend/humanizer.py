from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=GEMINI_API_KEY)
    logger.info("Gemini LLM configured for humanizer.")
else:
    logger.warning("GEMINI_API_KEY not found. Humanizer will not function without it.")
    llm = None # Or fallback to Ollama if desired, but for now, make it explicit it won't work.

class ArticleState:
    def __init__(self, original_article: str, humanized_article: str = "", feedback: str = "", iterations: int = 0):
        self.original_article = original_article
        self.humanized_article = humanized_article
        self.feedback = feedback
        self.iterations = iterations

    def to_dict(self):
        return {
            "original_article": self.original_article,
            "humanized_article": self.humanized_article,
            "feedback": self.feedback,
            "iterations": self.iterations
        }

    @staticmethod
    def from_dict(data: dict):
        return ArticleState(
            original_article=data["original_article"],
            humanized_article=data.get("humanized_article", ""),
            feedback=data.get("feedback", ""),
            iterations=data.get("iterations", 0)
        )

def humanizer_agent(state: ArticleState):
    if not llm:
        return ArticleState.from_dict({"error": "LLM not configured."})

    original_article = state.original_article
    current_humanized_article = state.humanized_article
    feedback = state.feedback

    if current_humanized_article and feedback:
        # Refine based on feedback
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert humanizer of technical articles. Your goal is to rewrite the provided article to have a human-like tone, incorporating frustration, jokes, and emotions, while strictly preserving the original meaning and all technical details. You have received feedback on a previous attempt. Incorporate this feedback to improve the humanization."),
            ("human", "Original Article:\n{original_article}\n\nPrevious Humanized Version:\n{current_humanized_article}\n\nFeedback:\n{feedback}\n\nBased on the feedback, provide an improved humanized version of the article. Ensure the meaning and technical details are unchanged, only the tone is adjusted.")
        ])
        chain = prompt_template | llm | StrOutputParser()
        humanized_output = chain.invoke({
            "original_article": original_article,
            "current_humanized_article": current_humanized_article,
            "feedback": feedback
        })
    else:
        # Initial humanization
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert humanizer of technical articles. Your goal is to rewrite the provided article to have a human-like tone, incorporating frustration, jokes, and emotions, while strictly preserving the original meaning and all technical details."),
            ("human", "Original Article:\n{original_article}\n\nProvide a humanized version of the article. Ensure the meaning and technical details are unchanged, only the tone is adjusted.")
        ])
        chain = prompt_template | llm | StrOutputParser()
        humanized_output = chain.invoke({"original_article": original_article})

    return ArticleState(
        original_article=original_article,
        humanized_article=humanized_output,
        feedback="", # Clear feedback after processing
        iterations=state.iterations + 1
    )

def evaluator_agent(state: ArticleState):
    if not llm:
        return ArticleState.from_dict({"error": "LLM not configured."})

    original_article = state.original_article
    humanized_article = state.humanized_article

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert evaluator of humanized technical articles. Your task is to provide constructive feedback on how well the 'Humanized Article' maintains the original meaning and technical details of the 'Original Article', and how effectively it incorporates human-like tone (frustration, jokes, emotions). Provide specific, actionable feedback for improvement. If the humanized article is perfect, state 'PERFECT'."),
        ("human", "Original Article:\n{original_article}\n\nHumanized Article:\n{humanized_article}\n\nProvide feedback for improvement, or state 'PERFECT' if no improvements are needed.")
    ])
    chain = prompt_template | llm | StrOutputParser()
    feedback = chain.invoke({
        "original_article": original_article,
        "humanized_article": humanized_article
    })

    return ArticleState(
        original_article=original_article,
        humanized_article=humanized_article,
        feedback=feedback,
        iterations=state.iterations
    )

def should_continue(state: ArticleState):
    if state.feedback == "PERFECT" or state.iterations >= 3: # Limit iterations to prevent infinite loops
        return "end"
    return "continue"

# Define the graph
workflow = StateGraph(ArticleState)

# Add nodes
workflow.add_node("humanizer", humanizer_agent)
workflow.add_node("evaluator", evaluator_agent)

# Set entry point
workflow.set_entry_point("humanizer")

# Add edges
workflow.add_edge("humanizer", "evaluator")
workflow.add_conditional_edges(
    "evaluator",
    should_continue,
    {
        "continue": "humanizer",
        "end": END
    }
)

app = workflow.compile()

def humanize_article_with_langgraph(original_article: str):
    initial_state = ArticleState(original_article=original_article)
    final_state = None
    for s in app.stream(initial_state):
        final_state = list(s.values())[0] # Get the state from the current step
        logger.info(f"Current state after iteration {final_state.iterations}: {final_state.to_dict()}")
    
    if final_state:
        return final_state.to_dict()
    return {"error": "Failed to humanize article."}

if __name__ == "__main__":
    # Example usage
    test_article = """
    The recent advancements in quantum computing have opened new avenues for solving complex computational problems that are intractable for classical computers. Quantum algorithms, such as Shor's algorithm for factoring large numbers and Grover's algorithm for searching unsorted databases, demonstrate the potential for exponential speedups. However, building stable and scalable quantum computers remains a significant engineering challenge due to issues like decoherence and error correction. Researchers are actively exploring various qubit technologies, including superconducting circuits, trapped ions, and topological qubits, to overcome these hurdles. The development of quantum software and programming languages is also crucial for harnessing the power of these nascent machines.
    """
    print("Starting humanization process...")
    result = humanize_article_with_langgraph(test_article)
    print("\n--- Final Humanized Article ---")
    print(result.get("humanized_article", "No humanized article found."))
    print(f"\nIterations: {result.get('iterations', 0)}")
    print(f"Final Feedback: {result.get('feedback', 'N/A')}")
