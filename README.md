# Streamlit App Hub: AI & Utility Tools

This project is a collection of useful tools and AI-powered applications built using Streamlit. It demonstrates the integration of various APIs (Google, OpenAI, X) and functionalities within a multi-page Streamlit application, supporting multiple generative models.

---

## Features

The hub currently includes the following tools:

1. **🏠 Mortgage Calculator**
   Calculate monthly mortgage payments and generate an amortization schedule.

2. **💬 Chatbot**
   Interact with various AI chat models powered by Large Language Models (LLMs).

3. **🖼️ Multimodal Query**
   Query language models with both text and optional image inputs (utilizing vision-capable LLMs).

4. **🎨 Image Generator**
   Generate images from text prompts using text-to-image models.

5. **📲 Tweet Generator**
   Create tweet suggestions based on personality, content type, and format, with an option to post directly to X (Twitter).

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

- **Python:** Version 3.9 or higher recommended.
- **Poetry:** A Python dependency management tool. ([Installation Guide](https://python-poetry.org/docs/#installation))

### Installation Steps

1. **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies using Poetry:**
    This command reads the `pyproject.toml` file and installs the required packages into a virtual environment.
    ```bash
    poetry install
    ```

---

## Configuration: API Keys & Supported Models

This project requires API keys for the generative model providers and X (Twitter) functionalities.

### Setting Up API Keys

1. **Create a `.env` file** in the root directory of the project.
2. **Add the following environment variables** to the `.env` file, replacing the placeholder values with your actual keys and secrets:

    ```dotenv
    # --- Google Gemini & Imagen API ---
    GEMINI_API_KEY="your_gemini_api_key"
    GEMINI_BASE_URL="your_custom_gemini_base_url"

    # --- OpenAI API ---
    OPENAI_API_KEY="your_openai_api_key"
    OPENAI_BASE_URL="your_custom_openai_base_url"

    # --- X (Twitter) API ---
    X_USERNAME="your_x_username"
    X_API_KEY="your_x_api_key"
    X_API_KEY_SECRET="your_x_api_key_secret"
    X_ACCESS_TOKEN="your_x_access_token"
    X_ACCESS_TOKEN_SECRET="your_x_access_token_secret"
    # Optional: Primarily for OAuth 2.0 authentication flows
    # X_CLIENT_ID="your_x_client_id"
    # X_CLIENT_SECRET="your_x_client_secret"
    ```

3. **Supported Models (as configured in `models/llm.py`):**

    - **Google (Requires `GEMINI_API_KEY`)**
        - Text Models:
            - `Gemini 2.0 Flash`
            - `Gemini 2.0 Flash Lite`
        - Image Models:
            - `Imagen 3` (`imagen-3-generate-002`)
    - **OpenAI (Requires `OPENAI_API_KEY`)**
        - Text Models:
            - `GPT-4o`
            - `GPT-4o Mini`
        - Image Models:
            - `DALL·E 3`

---

## Running the Application

1. **Activate the Poetry virtual environment:**
    ```bash
    poetry shell
    ```

2. **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```

    This will start the Streamlit server, and the application should open automatically in your default web browser. You can typically access it at `http://localhost:8501`.

---

## Future Improvements

- Expand multimodal support to more models.
- Add more robust error handling and user feedback across all tools.
- Implement comprehensive unit and integration tests.
- Refine UI/UX based on user feedback.
- Add more tools and model providers.

---

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
