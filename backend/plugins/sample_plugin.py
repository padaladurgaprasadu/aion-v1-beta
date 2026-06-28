from langchain.tools import tool

@tool
def hello_world_plugin(name: str) -> str:
    """A sample AiON enterprise plugin that says hello."""
    return f"Hello, {name}! This is a custom AiON plugin."

def register_tools():
    """Returns a list of LangChain tools to be injected into AiON."""
    return [hello_world_plugin]
