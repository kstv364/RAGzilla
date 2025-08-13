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

app = gr.TabbedInterface(
    [pdf_upload_interface, youtube_ingest_interface, qa_interface],
    ["Upload PDF", "Ingest YouTube", "Ask Questions"]
)

if __name__ == "__main__":
    GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))
    app.launch(server_port=GRADIO_PORT, server_name="0.0.0.0", share=True)
