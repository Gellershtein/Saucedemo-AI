"""
Wrapper for PyCharm External Tool to safely pass selected text
to ai_code_review.py using a temporary file.
"""
import sys
import os
import tempfile
import subprocess

# 1. Читаем выделенный текст
selected_text = ""
if len(sys.argv) > 1:
    selected_text = sys.argv[1]
else:
    print("❌ Ошибка: нет выделенного текста")
    sys.exit(1)

# 2. Создаём временный файл
with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False, encoding="utf-8") as tmp_file:
    tmp_file.write(selected_text)
    tmp_path = tmp_file.name

# 3. Путь к твоему ai_code_review.py
script_path = os.path.join(os.path.dirname(__file__), "ai_code_review.py")

# 4. Запускаем ai_code_review.py с временным файлом как аргумент
subprocess.run([sys.executable, script_path, tmp_path])

# 5. Опционально: удаляем временный файл
os.remove(tmp_path)
