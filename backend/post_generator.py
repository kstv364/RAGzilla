from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=GEMINI_API_KEY)
    logger.info("Gemini LLM configured for post generation and humanization.");
else:
    logger.warning("GEMINI_API_KEY not found. Post generator will not function without it.")
    llm = None

class PostState:
    def __init__(self, content: str, user_prompt: str, raw_posts: list = None, humanized_posts: list = None, feedback: list = None, iterations: int = 0):
        self.content = content
        self.user_prompt = user_prompt
        self.raw_posts = raw_posts if raw_posts is not None else []
        self.humanized_posts = humanized_posts if humanized_posts is not None else []
        self.feedback = feedback if feedback is not None else []
        self.iterations = iterations

    def to_dict(self):
        return {
            "content": self.content,
            "user_prompt": self.user_prompt,
            "raw_posts": self.raw_posts,
            "humanized_posts": self.humanized_posts,
            "feedback": self.feedback,
            "iterations": self.iterations
        }

    @staticmethod
    def from_dict(data: dict):
        return PostState(
            content=data["content"],
            user_prompt=data["user_prompt"],
            raw_posts=data.get("raw_posts", []),
            humanized_posts=data.get("humanized_posts", []),
            feedback=data.get("feedback", []),
            iterations=data.get("iterations", 0)
        )

def generate_posts_agent(state: PostState):
    if not llm:
        return PostState.from_dict({"error": "LLM not configured."})

    content = state.content
    user_prompt = state.user_prompt

    post_generation_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI/ML thought leader. Your task is to generate 3 distinct short posts (50-100 words each) based on the provided content and user prompt. Each post should:
            - Focus on AI/ML concepts.
            - Be insightful and demonstrate technical leadership.
            - Be concise and suitable for platforms like LinkedIn.
            - Incorporate the user's specific prompt or focus.
            - Use professional emojis sparingly to enhance readability and engagement.
            - Be structured with appropriate spacing (e.g., short paragraphs, line breaks) for a clean, catchy presentation on LinkedIn.
            - The English used should reflect that of a non-native Indian speaker, with subtle nuances in phrasing and vocabulary.
            - Each post should address the broad concept from a different angle or perspective
"""),
        ("human", """Content:\n{content}\n\nUser Prompt:\n{user_prompt}\n\n
         Generate 3 posts, each clearly separated by "---POST---".]\n\n
Example format:
Post 1 content.
---POST---
Post 2 content.
---POST---
Post 3 content.
         """)
    ])
    chain = post_generation_prompt | llm | StrOutputParser()
    posts_output = chain.invoke({"content": content, "user_prompt": user_prompt})
    posts = [p.strip() for p in posts_output.split("---POST---") if p.strip()]
    return PostState(content=content, user_prompt=user_prompt, raw_posts=posts, iterations=state.iterations)

def humanizer_agent(state: PostState):
    if not llm:
        return PostState.from_dict({"error": "LLM not configured."})

    raw_posts = state.raw_posts
    humanized_posts = []
    
    humanizer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert humanizer of technical articles. Your goal is to rewrite the provided article to have a human-like tone, incorporating frustration, jokes, and emotions, while strictly preserving the original meaning and all technical details. The English used should reflect that of a non-native Indian speaker, with subtle nuances in phrasing and vocabulary. Use professional emojis sparingly to enhance readability and engagement. Be structured with appropriate spacing (e.g., short paragraphs, line breaks) for a clean, catchy presentation."),
        ("human", "Original Article:\n{original_article}\n\nProvide a humanized version of the article. Ensure the meaning and technical details are unchanged, only the tone is adjusted.")
    ])
    chain = humanizer_prompt | llm | StrOutputParser()

    for post in raw_posts:
        humanized_output = chain.invoke({"original_article": post})
        humanized_posts.append(humanized_output)

    return PostState(content=state.content, user_prompt=state.user_prompt, raw_posts=raw_posts, humanized_posts=humanized_posts, iterations=state.iterations + 1)

def evaluator_agent(state: PostState):
    if not llm:
        return PostState.from_dict({"error": "LLM not configured."})

    raw_posts = state.raw_posts
    humanized_posts = state.humanized_posts
    feedback_list = []

    evaluator_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert evaluator of humanized technical articles. Your task is to provide constructive feedback on how well the 'Humanized Article' maintains the original meaning and technical details of the 'Original Article', and how effectively it incorporates human-like tone (frustration, jokes, and emotions). Provide feedback specific to LinkedIn, such as emoji usage, spacing, and overall presentation. If improvements are needed, provide specific, actionable feedback. If the humanized article is perfect, respond with ONLY the word 'PERFECT'."),
        ("human", "Original Article:\n{original_article}\n\nHumanized Article:\n{humanized_article}\n\nProvide feedback for improvement, or respond with ONLY the word 'PERFECT'.")
    ])
    chain = evaluator_prompt | llm | StrOutputParser()

    for i in range(len(raw_posts)):
        feedback = chain.invoke({
            "original_article": raw_posts[i],
            "humanized_article": humanized_posts[i]
        })
        feedback_list.append(feedback)

    return PostState(content=state.content, user_prompt=state.user_prompt, raw_posts=raw_posts, humanized_posts=humanized_posts, feedback=feedback_list, iterations=state.iterations + 1)

def should_continue(state: PostState):
    if state.iterations >= 2 or (state.feedback and all(f == "PERFECT" for f in state.feedback)):
        return "end"
    return "continue"

def write_posts_to_file(humanized_posts: list):
    import uuid
    import os

    base_dir = "summaries"
    output_dir = os.path.join(base_dir, "ai_ml_posts")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"ai_ml_posts_{str(uuid.uuid4())}.md"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding='utf-8') as f:
        for i, post in enumerate(humanized_posts):
            f.write(f"### Post {i+1}\n")
            f.write(post)
            f.write("\n\n")
    logger.info(f"AI/ML posts saved to {file_path}")
    return file_path

# Define the graph
workflow = StateGraph(PostState)

# Add nodes
workflow.add_node("generate_posts", generate_posts_agent)
workflow.add_node("humanizer", humanizer_agent)
workflow.add_node("evaluator", evaluator_agent)

# Set entry point
workflow.set_entry_point("generate_posts")

# Add edges
workflow.add_edge("generate_posts", "humanizer")
workflow.add_edge("humanizer", "evaluator")
workflow.add_conditional_edges(
    "evaluator",
    should_continue,
    {
        "continue": "humanizer",
        "end": END
    }
)

# Compile the graph
app = workflow.compile()

def generate_and_humanize_posts(content: str, user_prompt: str):
    initial_state = PostState(content=content, user_prompt=user_prompt)
    final_state = None
    try:
        for s in app.stream(initial_state):
            final_state = list(s.values())[0]
            logger.info(f"Current state after iteration {final_state.iterations}: {final_state.to_dict()}")
    except Exception as e:
        logger.error(f"LangGraph stream error: {e}")
        return {"error": f"Failed to generate and humanize posts: {e}"}

    if final_state and final_state.humanized_posts:
        file_path = write_posts_to_file(final_state.humanized_posts)
        return {"posts": final_state.humanized_posts, "file_path": file_path}
    return {"error": "Failed to generate and humanize posts."}

if __name__ == "__main__":
    # Example usage
    test_content = "The recent advancements in quantum computing have opened new avenues..."
    test_prompt = "Focus on the potential impact on cybersecurity."
    result = generate_and_humanize_posts(test_content, test_prompt)
    print(result)
