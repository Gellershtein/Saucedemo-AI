"""
AI Code Review Tool for PyCharm (Single-file version)

HOW TO USE:
1. Put this file anywhere (e.g. utils/ai_code_review.py)
2. Put config.json near
3. PyCharm → Settings → Tools → External Tools
4. Enable "Pass selected text to stdin"
"""

import sys
import json
import time
from typing import Dict
import os
from dotenv import load_dotenv

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
MAX_CODE_FALLBACK = 12000

PROMPT = """
        Ты — опытный Senior QA Automation Engineer и архитектор программного обеспечения.
    Твоя задача — выполнить код-ревью автотеста, анализируя его намерение и логику.
    Код может содержать синтаксические ошибки, незакрытые кавычки, незавершённые конструкции
    или внешние переменные — все такие проблемы необходимо ИГНОРИРОВАТЬ.
    
    Отвечай строго на русском языке.
    
    КОД ДЛЯ АНАЛИЗА:
    ```python
    {code}
    ```
    
    КРИТЕРИИ ОЦЕНКИ:
    1. НАДЁЖНОСТЬ И СТАБИЛЬНОСТЬ  
       (flaky-поведение, ожидания, асинхронность, стабильность выполнения)
    
    2. ПРОВЕРКИ И ВЕРИФИКАЦИЯ  
       (наличие assert’ов, корректность проверок, полнота валидации результата)
    
    3. ЧИТАЕМОСТЬ И ПОНЯТНОСТЬ  
       (именование, структура, самодокументируемость, ясность намерений)
    
    4. ХАРДКОД И ТЕСТОВЫЕ ДАННЫЕ  
       (магические строки/числа, фикстуры, конфигурации)
    
    5. ПОВТОРЯЕМОСТЬ И ПРИНЦИП DRY  
       (дублирование логики, переиспользование кода, хелперы)
    
    6. АРХИТЕКТУРА ТЕСТОВ  
       (POM или аналоги, разделение ответственности, масштабируемость)
    
    УРОВНИ ОЦЕНКИ (SEVERITY):
    - ❌ Критично (BLOCKER) — блокирует приёмку кода
    - ⚠️ Требует внимания (WARNING) — желательно исправить
    - ℹ️ Рекомендация (INFO) — улучшение качества
    - 🚫 Недостаточно данных (ERROR) — невозможно оценить критерий
    
    ПРАВИЛА АНАЛИЗА:
    - Игнорируй все синтаксические ошибки и неполный код
    - Фокусируйся только на логике и намерении теста
    - Если по критерию недостаточно данных — укажи статус 🚫 и явно напиши об этом
    - Комментарии должны быть краткими, практичными и конкретными
    - Общая оценка выставляется по шкале от 0 до 6
    - Итоговый вердикт REJECT — если есть хотя бы один ❌ BLOCKER
    
    ФОРМАТ ВЫВОДА (СТРОГО СОБЛЮДАТЬ):
    
    === РЕЗУЛЬТАТЫ КОД-РЕВЬЮ ===
    
    Основное намерение теста:
    [Кратко опиши, что именно проверяет данный тест]
    
    1. НАДЁЖНОСТЬ И СТАБИЛЬНОСТЬ  
    Статус: ✅ Отлично / ⚠️ Требует внимания / ❌ Критично / 🚫 Недостаточно данных  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    2. ПРОВЕРКИ И ВЕРИФИКАЦИЯ  
    Статус: ✅ / ⚠️ / ❌ / 🚫  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    3. ЧИТАЕМОСТЬ И ПОНЯТНОСТЬ  
    Статус: ✅ / ⚠️ / ❌ / 🚫  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    4. ХАРДКОД И ТЕСТОВЫЕ ДАННЫЕ  
    Статус: ✅ / ⚠️ / ❌ / 🚫  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    5. ПОВТОРЯЕМОСТЬ И ПРИНЦИП DRY  
    Статус: ✅ / ⚠️ / ❌ / 🚫  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    6. АРХИТЕКТУРА ТЕСТОВ  
    Статус: ✅ / ⚠️ / ❌ / 🚫  
    Комментарий:
    [Краткий анализ и конкретные рекомендации]
    
    ---
    ИТОГ:
    
    ОБЩАЯ ОЦЕНКА: [X]/6  
    FINAL VERDICT: APPROVE / REJECT  
    
    ПРИОРИТЕТНЫЕ ДЕЙСТВИЯ (ТОП-3):
    1. [Самое важное улучшение]
    2. [Второе по важности]
    3. [Третье по важности]
    
    КРАТКИЙ SUMMARY:
    [Один абзац с главным выводом и ключевым направлением улучшений]
"""


def call_openai(code: str, cfg: Dict) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=cfg["api_key"])
    r = client.chat.completions.create(
        model=cfg["model"],
        temperature=cfg.get("temperature", 0.2),
        max_tokens=cfg.get("max_tokens", 900),
        messages=[{"role": "user", "content": PROMPT.format(code=code)}]
    )
    return r.choices[0].message.content.strip()


def call_gemini(code: str, cfg: Dict) -> str:
    from google import genai
    client = genai.Client(api_key=cfg["api_key"])
    response = client.models.generate_content(
        model=cfg["model"],
        contents=[PROMPT.format(code=code)]
    )
    return response.candidates[0].content.parts[0].text.strip()


def call_mistral(code: str, cfg: Dict) -> str:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    client = MistralClient(api_key=cfg["api_key"])
    r = client.chat(
        model=cfg["model"],
        messages=[ChatMessage(role="user", content=PROMPT.format(code=code))]
    )
    return r.choices[0].message.content.strip()


def load_config() -> Dict:
    script_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(os.path.abspath(os.path.join(script_dir, '..', '..')), '.env')
    load_dotenv(dotenv_path=dotenv_path)

    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)

    config["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
    config["gemini"]["api_key"] = os.getenv("GEMINI_API_KEY")
    config["mistral"]["api_key"] = os.getenv("MISTRAL_API_KEY")

    return config


def read_selected_code() -> str:
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def safe_parse_json(raw: str) -> Dict:
    try:
        clean_str = raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_str)
    except Exception:
        return {
            "score": 0,
            "rules": [],
            "final_verdict": "REJECT",
            "summary": f"AI вернул некорректный JSON: {raw}"
        }


def print_result(result: Dict):
    icons = {"BLOCKER": "🔴", "WARNING": "🟡", "INFO": "🔵"}
    print("\n================ AI CODE REVIEW ================\n")
    print(f"ОБЩАЯ ОЦЕНКА: {result.get('score', 0)}/10\n")
    for rule in result.get("rules", []):
        sev = rule.get("severity", "INFO")
        print(f"{icons.get(sev, '⚪')} {rule.get('rule')}")
        print(f"   Severity: {sev}")
        print(f"   {rule.get('comment')}\n")
    verdict = result.get("final_verdict", "REJECT")
    verdict_icon = "✅" if verdict == "APPROVE" else "❌"
    print("------------------------------------------------")
    print(f"{verdict_icon} РЕЗУЛЬТАТ: {verdict}")
    print(f"ИТОГ: {result.get('summary')}")


def main():
    code = read_selected_code()
    if not code:
        print("❌ Ошибка: не передан код")
        return

    cfg = load_config()
    provider = cfg.get("provider")
    max_len = cfg.get("limits", {}).get("max_code_length", MAX_CODE_FALLBACK)
    if len(code) > max_len:
        code = code[:max_len]

    start = time.time()
    try:
        if provider == "openai":
            raw = call_openai(code, cfg["openai"])
        elif provider == "gemini":
            raw = call_gemini(code, cfg["gemini"])
        elif provider == "mistral":
            raw = call_mistral(code, cfg["mistral"])
        else:
            raise ValueError("Unknown provider")

        parsed = safe_parse_json(raw)
        print_result(parsed)
        print(f"\n⏱ Время анализа: {round(time.time() - start, 2)} сек")
    except Exception as e:
        print("⚠️ Ошибка при обращении к AI")
        print(str(e))


if __name__ == "__main__":
    main()