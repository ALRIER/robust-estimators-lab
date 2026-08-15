from pathlib import Path

path = Path("streamlit_app.py")
text = path.read_text(encoding="utf-8")
text = text.replace(
    "    import html as _html\n\n    note_section",
    "    import html as _html\n    import re as _re\n\n    note_section",
    1,
)
text = text.replace(
    'return [part.strip() for part in re.split(r"(?<=[.!?])\\s+", text_value) if part.strip()]',
    'return [part.strip() for part in _re.split(r"(?<=[.!?])\\s+", text_value) if part.strip()]',
    1,
)
path.write_text(text, encoding="utf-8")
print("Presenter runtime import fixed.")
