import language_tool_python

_tool_cache = {}

def get_tool(language: str = "en-US"):
    if language not in _tool_cache:
        _tool_cache[language] = language_tool_python.LanguageToolPublicAPI(language)  # uses public API
    return _tool_cache[language]

def check_text(text: str, language: str = "en-US"):
    tool = get_tool(language)
    matches = tool.check(text)
    return matches

def apply_corrections(text: str, matches):
    return language_tool_python.utils.correct(text, matches)
