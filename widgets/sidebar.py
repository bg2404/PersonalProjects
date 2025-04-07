import streamlit as st

from utils.api_client import get_api_client
from widgets.select_model import select_model


def setup_sidebar(model_options: dict):
    """
    Sets up the Streamlit sidebar for API model selection and client initialization.

    Args:
        model_options (dict): The dictionary of model options (e.g., TEXT_MODEL_OPTIONS).

    Returns:
        tuple: (selected_model_name, client_instance) or (None, None) if setup fails.
               Returns (None, None) and stops execution via st.stop() on critical errors.
    """
    with st.sidebar:
        st.header("Configuration")
        selected_model_name, api_config = select_model(model_options)
        api_name = api_config.get("name", "Selected API")
        api_key = api_config.get("key")
        api_url = api_config.get("url")

        if not api_key:
            # Determine expected env var for error message
            env_var_name = "OPENAI_API_KEY"  # Default assumption
            if "Gemini" in api_name:
                env_var_name = "GEMINI_API_KEY"
            elif "OpenAI" in api_name:
                env_var_name = "OPENAI_API_KEY"

            st.error(f"API Key for {api_name} not found.")
            st.info(f"Please ensure your `.env` file defines `{env_var_name}`.")
            if api_url:
                st.link_button(f"Get {api_name} API key", f"{api_url}", icon="🔑")
            st.stop()

        # Proactive warning for Imagen as it often requires billing setup
        if "imagen" in selected_model_name.lower():
            st.error(
                f"**Note:** Access to the **{api_name}** API typically requires a "
                f"Google Cloud account with **billing enabled**. Generation may fail "
                f"if billing is not active."
            )
            # Consider changing st.stop() to st.warning() if you want users to proceed anyway
            st.stop()

        client = get_api_client(api_config)
        if not client:
            st.error("Failed to initialize API client. Check configuration and logs.")
            st.stop()

        return selected_model_name, client
