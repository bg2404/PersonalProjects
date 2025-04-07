from typing import Any, Dict, Tuple

import streamlit as st


def select_model(model_options: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Displays a selectbox for choosing a model and returns its details.

    Args:
        model_options (Dict[str, Model]): A dictionary where keys are model API names
                                          and values are Model objects.

    Returns:
        Tuple[str, Dict[str, Any]]: A tuple containing:
            - selected_model_name (str): The API identifier of the chosen model.
            - api_config (dict): The API configuration dictionary associated with the model.
    """
    selected_model_name = st.selectbox(
        "Select a model",
        options=model_options.keys(),
        format_func=lambda model_api_name: model_options[model_api_name].name,
        help="Select the AI model to use.",
    )
    model = model_options[selected_model_name]

    # Only show button if URL is defined in API config
    if model.api.get("url"):
        st.link_button(f"Get {model.api['name']} API key", f"{model.api['url']}", icon="🔑")

    return selected_model_name, model.api
