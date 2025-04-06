import os
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API = {
    "name": "Gemini",
    "key": os.getenv("GEMINI_API_KEY"),
    "url": os.getenv("GEMINI_API_URL", "https://aistudio.google.com/app/apikey"),
    "base_url": os.getenv("GEMINI_BASE_URL"),
}
OPENAI_API = {
    "name": "OpenAI",
    "key": os.getenv("OPENAI_API_KEY"),
    "url": os.getenv("OPENAI_API_URL", "https://platform.openai.com/api-keys"),
    "base_url": os.getenv("OPENAI_BASE_URL"),
}

class Model:
    """Represents an AI model with its configuration."""
    name: str       # User-friendly display name (e.g., "GPT-4o")
    model_name: str # API identifier (e.g., "gpt-4o")
    api: dict       # Associated API configuration (GEMINI_API or OPENAI_API)

    def __init__(self, name, model_name, api):
        self.name = name
        self.model_name = model_name
        self.api = api

    def __repr__(self):
        return f"Model(name={self.name}, model_name={self.model_name})"

    def __str__(self):
        return self.name

# Text Models
GEMINI_2_0_FLASH = Model(
    name="Gemini 2.0 Flash",
    model_name="gemini-2.0-flash",
    api=GEMINI_API,
)
GEMINI_2_0_FLASH_LITE = Model(
    name="Gemini 2.0 Flash Lite",
    model_name="gemini-2.0-flash-lite",
    api=GEMINI_API,
)
GPT_4O = Model(
    name="GPT-4o",
    model_name="gpt-4o",
    api=OPENAI_API,
)
GPT_4O_MINI = Model(
    name="GPT-4o Mini",
    model_name="gpt-4o-mini",
    api=OPENAI_API,
)

# Image Generation Models
DALL_E_3 = Model(
    name="DALL-E 3",
    model_name="dall-e-3",
    api=OPENAI_API,
)
IMAGEN_3_GENERATE_002 = Model(
    name="Imagen 3",
    model_name="imagen-3.0-generate-002",
    api=GEMINI_API,
)

TEXT_MODEL_OPTIONS = {
    GEMINI_2_0_FLASH.model_name: GEMINI_2_0_FLASH,
    GEMINI_2_0_FLASH_LITE.model_name: GEMINI_2_0_FLASH_LITE,
    GPT_4O.model_name: GPT_4O,
    GPT_4O_MINI.model_name: GPT_4O_MINI,
}

IMAGE_MODEL_OPTIONS = {
    DALL_E_3.model_name: DALL_E_3,
    IMAGEN_3_GENERATE_002.model_name: IMAGEN_3_GENERATE_002,
}
