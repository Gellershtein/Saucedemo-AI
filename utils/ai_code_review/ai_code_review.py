"""
AI Code Review Tool for PyCharm
Text-only mode. NO JSON. NO verdict enforcement.
"""

import os
import time
import json
from typing import Dict
from dotenv import load_dotenv

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "qa_code_review_prompt.txt")
MAX_CODE_FALLBACK = 12000


def load_prompt() -> str:
    with open(PROMPT_FILE, encoding="utf-8") as f:
        return f.read()


def load_config() -> Dict:
    load_dotenv()
    with open(CONFIG_FILE, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
    cfg["gemini"]["api_key"] = os.getenv("GEMINI_API_KEY")
    cfg["mistral"]["api_key"] = os.getenv("MISTRAL_API_KEY")
    return cfg


def read_selected_code() -> str:
    import pyperclip
    return pyperclip.paste()


def call_openai(code: str, cfg: Dict, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=cfg["api_key"])
    r = client.chat.completions.create(
        model=cfg["model"],
        temperature=0.2,
        max_tokens=900,
        messages=[{"role": "user", "content": prompt.format(code=code)}]
    )
    return r.choices[0].message.content.strip()


def call_gemini(code: str, cfg: Dict, prompt: str) -> str:
    from google import genai
    client = genai.Client(api_key=cfg["api_key"])
    r = client.models.generate_content(
        model=cfg["model"],
        contents=[prompt.format(code=code)]
    )
    return r.candidates[0].content.parts[0].text.strip()


def call_mistral(code: str, cfg: Dict, prompt: str) -> str:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    client = MistralClient(api_key=cfg["api_key"])
    r = client.chat(
        model=cfg["model"],
        messages=[ChatMessage(role="user", content=prompt.format(code=code))]
    )
    return r.choices[0].message.content.strip()


def main():
    code = read_selected_code()
    if not code.strip():
        print("❌ Ошибка: не передан код для анализа")
        return

    cfg = load_config()
    prompt = load_prompt()
    provider = cfg.get("provider")
    code = code[:MAX_CODE_FALLBACK]

    start = time.time()
    if provider == "openai":
        result = call_openai(code, cfg["openai"], prompt)
    elif provider == "gemini":
        result = call_gemini(code, cfg["gemini"], prompt)
    elif provider == "mistral":
        result = call_mistral(code, cfg["mistral"], prompt)
    else:
        raise ValueError("Unknown provider")

    print("\n================ AI CODE REVIEW ================\n")
    print(result)
    print(f"\n⏱ Время анализа: {round(time.time() - start, 2)} сек")


if __name__ == "__main__":
    main()
