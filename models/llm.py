import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")


class Model:

    name: str
    model: str
    api_key: str
    api_key_url: str

    def __init__(self, name, model, api_key, api_key_url):
        self.name = name
        self.model = model
        self.api_key = api_key
        self.api_key_url = api_key_url

    def __repr__(self):
        return f"Model(name={self.name}, model={self.model})"

    def __str__(self):
        return self.name


GEMINI_2_0_FLASH = Model(
    name="Gemini 2.0 Flash",
    model="gemini-2.0-flash",
    api_key=GEMINI_API_KEY,
    api_key_url=GEMINI_API_URL,
)
GEMINI_2_0_FLASH_LITE = Model(
    name="Gemini 2.0 Flash Lite",
    model="gemini-2.0-flash-lite",
    api_key=GEMINI_API_KEY,
    api_key_url=GEMINI_API_URL,
)
GPT_4O = Model(
    name="GPT-4o",
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    api_key_url=OPENAI_API_URL,
)
GPT_4O_MINI = Model(
    name="GPT-4o Mini",
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    api_key_url=OPENAI_API_URL,
)

MODEL_OPTIONS = {
    GEMINI_2_0_FLASH.model: GEMINI_2_0_FLASH,
    GEMINI_2_0_FLASH_LITE.model: GEMINI_2_0_FLASH_LITE,
    GPT_4O.model: GPT_4O,
    GPT_4O_MINI.model: GPT_4O_MINI,
}