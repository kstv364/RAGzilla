import gradio as gr
import requests

import os
API_BASE = os.getenv("API_BASE", "http://localhost:8000")

def upload_pdf(file, collection_name_input, add_to_kb):
    if file is None:
        return {"error": "Please upload a PDF file."}
    if add_to_kb and collection_name_input == "temp_docs":
        return {"error": "Collection name 'temp_docs' cannot be used for persistent knowledge base."}
    collection_name = collection_name_input if add_to_kb else "temp_docs"
    with open(file.name, "rb") as f:
        response = requests.post(f"{API_BASE}/ingest-pdf", files={"file": (file.name, f)}, data={"collection_name": collection_name})
    return response.json()

def ingest_youtube_video(youtube_url, collection_name_input, add_to_kb, summary_type):
    if not youtube_url:
        return {"error": "Please enter a YouTube URL."}, "No summary available."
    if add_to_kb and collection_name_input == "temp_docs":
        return {"error": "Collection name 'temp_docs' cannot be used for persistent knowledge base."}, "No summary available."
    collection_name = collection_name_input if add_to_kb else "temp_docs"
    response = requests.post(
        f"{API_BASE}/ingest-youtube",
        data={
            "youtube_url": youtube_url,
            "collection_name": collection_name,
            "summary_type": summary_type # Pass the summary type
        }
    )
    result = response.json()
    summary = result.pop("summary", "No summary available.") # Remove summary from result JSON
    return result, summary

def ask_question(question, collection_name_input):
    collection_name = collection_name_input if collection_name_input else "docs" # Default to 'docs' for general Q&A
    print(f"Asking question: {question} from collection: {collection_name}")
    response = requests.get(f"{API_BASE}/ask", params={"query": question, "collection_name": collection_name})
    return response.json().get("answer", "No answer returned")

# PDF Ingest Interface
pdf_upload_interface = gr.Interface(
    fn=upload_pdf,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Textbox(label="Knowledge Base Name (e.g., my_project_kb)", value="temp_docs"),
        gr.Checkbox(label="Add to Knowledge Base (persistent)", value=True)
    ],
    outputs=gr.JSON(label="Upload Result"),
    title="PDF Ingest"
)

# YouTube Ingest Interface
with gr.Blocks() as youtube_ingest_interface:
    gr.Markdown("## YouTube Ingest")
    youtube_url_input = gr.Textbox(label="YouTube URL")
    collection_name_input = gr.Textbox(label="Knowledge Base Name (e.g., my_youtube_kb)", value="youtube_docs")
    add_to_kb_checkbox = gr.Checkbox(label="Add to Knowledge Base (persistent)", value=True)

    summary_type_main = gr.Radio(
        ["Study Guide", "Detailed Transcript", "Medium Article"],
        label="Output Type",
        value="Study Guide",
        info="Choose the desired output format."
    )

    medium_article_expertise = gr.Radio(
        ["Cloud Expertise", "AI/ML Expertise"],
        label="Medium Article Expertise",
        visible=False, # Hidden by default
        info="Choose the expertise area for the Medium article."
    )

    # Function to update visibility of expertise radio buttons
    def update_expertise_visibility(choice):
        if choice == "Medium Article":
            return gr.update(visible=True)
        else:
            return gr.update(visible=False)

    summary_type_main.change(
        update_expertise_visibility,
        inputs=summary_type_main,
        outputs=medium_article_expertise
    )

    # State to hold the dynamically determined summary type
    final_summary_type_state = gr.State(value="study_guide")

    # Function to determine the final summary_type to send to backend
    def update_final_summary_type(main_type, expertise_type):
        if main_type == "Study Guide":
            return "study_guide"
        elif main_type == "Detailed Transcript":
            return "detailed_transcript"
        elif main_type == "Medium Article":
            if expertise_type == "Cloud Expertise":
                return "medium_article_cloud"
            elif expertise_type == "AI/ML Expertise":
                return "medium_article_ai_ml"
        return "study_guide" # Default fallback

    summary_type_main.change(
        fn=update_final_summary_type,
        inputs=[summary_type_main, medium_article_expertise],
        outputs=final_summary_type_state
    )

    medium_article_expertise.change(
        fn=update_final_summary_type,
        inputs=[summary_type_main, medium_article_expertise],
        outputs=final_summary_type_state
    )

    ingest_button = gr.Button("Ingest and Summarize")

    ingest_result_json = gr.JSON(label="Ingest Result")
    video_summary_markdown = gr.Markdown(label="Generated Output")

    ingest_button.click(
        fn=ingest_youtube_video,
        inputs=[
            youtube_url_input,
            collection_name_input,
            add_to_kb_checkbox,
            final_summary_type_state # Pass the state directly
        ],
        outputs=[ingest_result_json, video_summary_markdown]
    )

# Q&A Interface
qa_interface = gr.Interface(
    fn=ask_question,
    inputs=[
        gr.Textbox(label="Ask a Question"),
        gr.Textbox(label="Knowledge Base Name (optional, leave blank for default 'temp_docs')", value="temp_docs")
    ],
    outputs=gr.Markdown(label="Answer"),
    title="Ask Questions from Knowledge Bases"
)

# Humanizer Interface
humanizer_interface = gr.Interface(
    fn=lambda x: requests.post(f"{API_BASE}/humanize-article", data={"original_article": x}).json().get("humanized_article", "Error humanizing article."),
    inputs=gr.Textbox(label="Original Article", lines=10),
    outputs=gr.Markdown(label="Humanized Article"),
    title="Humanize Medium Article"
)

# Post Generation Interface
with gr.Blocks() as post_generation_interface:
    gr.Markdown("## Generate AI/ML Thought Leader Posts")
    youtube_url_input_posts = gr.Textbox(label="YouTube URL (Optional)", placeholder="Enter YouTube URL or provide text below")
    text_input_posts = gr.Textbox(label="Text Input (Optional)", lines=5, placeholder="Enter text directly if no YouTube URL")
    user_prompt_posts = gr.Textbox(label="User Prompt", placeholder="e.g., 'Focus on recent advancements in LLMs' or 'Explain the challenges of MLOps'")
    
    generate_posts_button = gr.Button("Generate Posts")
    
    output_post_1 = gr.Markdown("### Post 1")
    output_post_content_1 = gr.Markdown(label="Content")
    output_post_2 = gr.Markdown("### Post 2")
    output_post_content_2 = gr.Markdown(label="Content")
    output_post_3 = gr.Markdown("### Post 3")
    output_post_content_3 = gr.Markdown(label="Content")

    def generate_posts_frontend(youtube_url, text_input, user_prompt):
        payload = {
            "user_prompt": user_prompt
        }
        if youtube_url:
            payload["youtube_url"] = youtube_url
        elif text_input:
            payload["text_input"] = text_input
        else:
            return "Error: Either YouTube URL or text input must be provided.", "", ""

        response = requests.post(f"{API_BASE}/generate-posts", data=payload)
        result = response.json()
        
        if "error" in result:
            return result["error"], "", ""
        
        posts = result.get("posts", [])
        return "", posts[0] if len(posts) > 0 else "", \
               "", posts[1] if len(posts) > 1 else "", \
               "", posts[2] if len(posts) > 2 else ""

    generate_posts_button.click(
        fn=generate_posts_frontend,
        inputs=[youtube_url_input_posts, text_input_posts, user_prompt_posts],
        outputs=[output_post_1, output_post_content_1,
                 output_post_2, output_post_content_2,
                 output_post_3, output_post_content_3]
    )

app = gr.TabbedInterface(
    [pdf_upload_interface, youtube_ingest_interface, qa_interface, humanizer_interface, post_generation_interface],
    ["Upload PDF", "Ingest YouTube", "Ask Questions", "Humanize Article", "Generate AI/ML Posts"]
)

if __name__ == "__main__":
    GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))
    app.launch(server_port=GRADIO_PORT, server_name="0.0.0.0", share=True)
