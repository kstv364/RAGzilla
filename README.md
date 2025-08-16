# RAGzilla: AI-Powered Content Generation for Technical Thought Leadership

## Project Description

RAGzilla is a comprehensive solution designed to generate engaging and informative content for technical thought leaders, particularly in the AI/ML space. It leverages Retrieval-Augmented Generation (RAG) techniques, LangChain, and Google's Generative AI models to produce high-quality blog posts, LinkedIn updates, and study guides from various input sources, including YouTube videos and text. The project also incorporates iterative humanization to ensure the generated content aligns with the user's desired tone and style.

## Problems Solved

RAGzilla addresses several key challenges faced by technical professionals looking to establish themselves as thought leaders:

-   **Content Creation Bottleneck:** Overcoming the time-consuming and often challenging process of creating original, high-quality content.
-   **Maintaining a Consistent Voice:** Ensuring that generated content aligns with the user's personal brand and expertise.
-   **Generating Engaging Content:** Producing content that resonates with the target audience and sparks meaningful conversations.
-   **Leveraging Existing Content:** Repurposing existing content, such as YouTube videos, into different formats for broader reach.
-   **AI/ML Content Generation:** Generating AI/ML content that is accurate, informative, and engaging.

## Usage Instructions (Docker)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/kstv364/RAGzilla.git
    cd RAGzilla
    ```

2.  **Build the Docker images:**

    ```bash
    docker-compose build
    ```

3.  **Run the Docker containers:**

    ```bash
    docker-compose up -d
    ```

4.  **Access the Gradio UI:**

    Open your web browser and navigate to `http://localhost:7860`.

## Technologies Used

-   **LangChain:** A framework for developing applications powered by language models.
-   **LangGraph:** A library for building robust and modular conversational AI systems.
-   **Google Generative AI:** Google's suite of generative AI models, including Gemini.
-   **FastAPI:** A modern, high-performance web framework for building APIs.
-   **Gradio:** A library for creating customizable UI components for machine learning models.
-   **Sentence Transformers:** A library for generating sentence embeddings.
-   **Qdrant:** A vector database for storing and retrieving embeddings.
-   **Docker:** A platform for building, deploying, and running applications in containers.

## Project Structure

```
RAGzilla/
├── .gitignore
├── backend/
│   ├── .gitignore
│   ├── Dockerfile
│   ├── humanizer.py
│   ├── ingest.py
│   ├── llm_client.py
│   ├── main.py
│   ├── post_generator.py
│   ├── qdrant_client.py
│   ├── rag.py
│   ├── requirements.txt
├── docker/
│   ├── docker-compose.yml
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── qdrant-deployment.yaml
├── summaries/
│   ├── ai_ml_posts/
│   ├── detailed_transcripts/
│   ├── medium_articles_ai_ml/
│   ├── medium_articles_cloud/
│   ├── study_guides/
├── readme.md
```

## Contributing

Contributions are welcome! Please submit a pull request with your proposed changes.

## License

[MIT](https://opensource.org/licenses/MIT)
