# RAGzilla: AI-Powered Content Generation for Technical Thought Leadership


## 🚀 Project Overview

RAGzilla is an innovative and comprehensive solution designed to empower technical thought leaders, especially in the dynamic AI/ML domain, by streamlining the creation of engaging and informative content. Leveraging cutting-edge Retrieval-Augmented Generation (RAG) techniques, LangChain, and Google's Generative AI models, RAGzilla produces high-quality blog posts, LinkedIn updates, and study guides from diverse input sources, including YouTube videos and raw text. A unique feature of RAGzilla is its iterative humanization process, ensuring that the generated content perfectly aligns with the user's desired tone, style, and personal brand.

## ✨ Key Features & Benefits

-   **Automated Content Generation:** Effortlessly transform raw information into polished, publication-ready content.
-   **Personalized Voice & Style:** Maintain a consistent and authentic voice across all generated materials through iterative humanization.
-   **Multi-Source Ingestion:** Generate content from various inputs, including long-form YouTube videos (transcribed and summarized) and extensive text documents.
-   **Targeted Content Formats:** Produce tailored outputs such as in-depth blog posts, concise LinkedIn updates, and comprehensive study guides.
-   **AI/ML Specialization:** Specifically designed to handle complex AI/ML topics, ensuring accuracy and relevance.
-   **Scalable & Modular Architecture:** Built with Docker and Kubernetes readiness for easy deployment and scaling.

## 🎯 Problems Solved

RAGzilla directly addresses critical challenges faced by technical professionals aspiring to establish and maintain their thought leadership:

-   **Content Creation Bottleneck:** Eliminates the time-consuming and often daunting process of generating original, high-quality content from scratch.
-   **Brand Consistency:** Guarantees that all generated content reflects the user's unique personal brand and expertise, fostering trust and recognition.
-   **Audience Engagement:** Crafts compelling content that resonates with the target audience, sparking meaningful discussions and interactions.
-   **Content Repurposing:** Maximizes the value of existing assets by transforming them into new formats for broader reach and impact.
-   **Accuracy in Technical Content:** Ensures that AI/ML content is not only informative and engaging but also technically accurate and up-to-date.

## 🛠️ Technologies Used

RAGzilla is built upon a robust stack of modern technologies:

-   **LangChain:** A powerful framework for developing applications driven by large language models.
-   **LangGraph:** Enhances LangChain by enabling the creation of stateful, multi-actor applications with cycles.
-   **Google Generative AI:** Utilizes Google's advanced generative AI models, including the Gemini family, for content creation.
-   **FastAPI:** A high-performance, easy-to-use web framework for building the backend API.
-   **Gradio:** Facilitates rapid prototyping and deployment of the user-friendly web interface for interaction with the models.
-   **Sentence Transformers:** Employed for generating high-quality sentence embeddings, crucial for RAG.
-   **Qdrant:** A blazing-fast vector database used for efficient storage and retrieval of embeddings.
-   **Docker:** Containerization platform for consistent development, testing, and deployment environments.
-   **Kubernetes:** Orchestration system for automating deployment, scaling, and management of containerized applications.

## 🚀 Getting Started (Docker)

Follow these steps to get RAGzilla up and running quickly using Docker:

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

## 📂 Project Structure

```
RAGzilla/
├── .gitignore
├── LICENSE
├── README.md
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
│   └── requirements.txt
├── docker/
│   └── docker-compose.yml
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── qdrant-deployment.yaml
└── summaries/
    ├── ai_ml_posts/
    ├── detailed_transcripts/
    ├── medium_articles_ai_ml/
    ├── medium_articles_cloud/
    └── study_guides/
```

## 🤝 Contributing

We welcome contributions to RAGzilla! If you have ideas for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

Please ensure your code adheres to the existing style and includes appropriate tests.

## 📜 License

This project is distributed under a [Proprietary License](LICENSE). All rights reserved by Kaustav Chanda. Unauthorized use, copying, modification, or distribution is strictly prohibited.

## 📧 Contact

For any inquiries or support, please contact Kausstav Chanda at [kaustav.chanda.work@gmail.com]. <!-- Placeholder for your email -->
