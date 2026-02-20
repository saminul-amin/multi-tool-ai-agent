from langchain_community.tools import DuckDuckGoSearchRun

def get_web_search_tool():
    search = DuckDuckGoSearchRun(
        name="WebSearchTool",
        description=(
            "Search the web for general knowledge questions about Bangladesh "
            "that are NOT related to specific data in the institutions, hospitals, "
            "or restaurants databases. Use this for questions about policies, history, "
            "culture, demographics, government bodies, healthcare systems, education "
            "systems, or any other general information. "
            "Input should be a search query string."
        ),
    )
    return search
