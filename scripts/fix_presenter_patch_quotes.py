from pathlib import Path

path = Path("scripts/patch_presenter_notes.py")
text = path.read_text(encoding="utf-8")
text = text.replace("new_renderer = r'''# Presenter view:", 'new_renderer = r"""# Presenter view:', 1)
text = text.replace("    st.stop()\n'''\n\npattern = re.compile(", '    st.stop()\n"""\n\npattern = re.compile(', 1)
path.write_text(text, encoding="utf-8")
print("Presenter patch quoting repaired for this workflow run.")
