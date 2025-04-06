import streamlit as st
from openai import OpenAI, APIError, APITimeoutError

def get_api_client(api_config: dict):
    """
    Initializes and returns an API client based on the provided configuration.
    Manages client instances in Streamlit's session state.

    Args:
        api_config (dict): Dictionary containing API details ('key', 'base_url', 'name').

    Returns:
        An initialized API client instance (e.g., openai.OpenAI) or None if initialization fails.
    """
    api_key = api_config.get('key')
    base_url = api_config.get('base_url')
    api_name = api_config.get('name', 'UnknownAPI')
    client_session_key = f"api_client_{api_name}"
    config_session_key = f"{client_session_key}_config"

    # Check if a valid client already exists in session state for this config
    if client_session_key in st.session_state:
        stored_config = st.session_state.get(config_session_key, {})
        # Check if key and base_url match the current requirement
        if stored_config.get('key') == api_key and stored_config.get('base_url') == base_url:
            return st.session_state[client_session_key] # Return existing client

    st.sidebar.info(f"Initializing API client for {api_name}...")
    client = None
    try:
        if "OpenAI" in api_name or "DALL-E" in api_name or "ChatGPT" in api_name:
            effective_base_url = base_url if base_url else None
            client = OpenAI(api_key=api_key, base_url=effective_base_url)
            st.session_state[client_session_key] = client
            st.session_state[config_session_key] = {'key': api_key, 'base_url': base_url, 'name': api_name}
            st.sidebar.success(f"OpenAI client for {api_name} initialized.")

        elif "Gemini" in api_name or "Imagen" in api_name:
            effective_base_url = base_url if base_url else None
            if not effective_base_url:
                 st.error(f"Base URL is required for {api_name} but not found in config.")
                 return None
            # Attempting to use OpenAI client library for Google models. Ensure endpoint is compatible.
            client = OpenAI(api_key=api_key, base_url=effective_base_url)

            st.session_state[client_session_key] = client
            st.session_state[config_session_key] = {'key': api_key, 'base_url': base_url, 'name': api_name}
            st.sidebar.success(f"Client for {api_name} initialized (using OpenAI library).")

        else:
            st.sidebar.error(f"Client initialization not defined for API type: {api_name}")
            return None

        return client

    except APIError as e:
        st.sidebar.error(f"API Error during client initialization for {api_name}: {e}")
    except APITimeoutError as e:
         st.sidebar.error(f"API Timeout during client initialization for {api_name}: {e}")
    except Exception as e:
        st.sidebar.error(f"Failed to initialize API client for {api_name}: {e}")
        if client_session_key in st.session_state: del st.session_state[client_session_key]
        if config_session_key in st.session_state: del st.session_state[config_session_key]
        return None
