import streamlit as st

from utils.api_client import get_api_client

from utils.api_client import get_api_client
from widgets.select_model import select_model


class SidebarManager:
    def __init__(self, model_options):
        self.model_options = model_options

    def setup(self):
        with st.sidebar:
            st.header("Configuration")
            selected_model_name, api_config = select_model(self.model_options)
            self.validate_api_key(api_config)
            client = get_api_client(api_config)
            if not client:
                st.error("Failed to initialize API client. Check configuration and logs.")
                st.stop()
            return selected_model_name, client

    def validate_api_key(self, api_config):
        api_key = api_config.get("key")
        api_url = api_config.get("url")
        api_name = api_config.get("name", "Selected API")

        if not api_key:
            env_var_name = self.get_env_var_name(api_name)
            st.error(f"API Key for {api_name} not found.")
            st.info(f"Please ensure your `.env` file defines `{env_var_name}`.")
            if api_url:
                st.link_button(f"Get {api_name} API key", f"{api_url}", icon="🔑")
                st.link_button(f"Get {api_name} API key", f"{api_url}", icon="🔑")
            st.stop()

    def get_env_var_name(self, api_name):
        if "Gemini" in api_name:
            return "GEMINI_API_KEY"
        elif "OpenAI" in api_name:
            return "OPENAI_API_KEY"
        return "API_KEY"
