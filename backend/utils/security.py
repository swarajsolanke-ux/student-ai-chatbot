# security.py - Part of utils module
def sanitize(text: str) -> str:
    return text.replace("<", "").replace(">", "")
