# Multi-Tool AI Agent for Bangladesh

An AI-powered agent built with **LangChain** and **Streamlit** that answers data-specific queries from three Bangladesh datasets and uses web search for general knowledge questions — all through a chat interface.

![LLM](https://img.shields.io/badge/LLM-Qwen2.5--72B-blue?style=flat-square)
![Framework](https://img.shields.io/badge/Agent-LangChain_ReAct-orange?style=flat-square)
![Frontend](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat-square)
![Search](https://img.shields.io/badge/Search-DuckDuckGo-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square)

---

## Features

- **Intelligent Query Routing** — The ReAct agent automatically decides which tool to use based on your question.
- **3 Structured Database Tools** — Query real Bangladesh data on institutions, hospitals, and restaurants via natural language.
- **Web Search Fallback** — General knowledge questions are routed to DuckDuckGo search.
- **Chat Interface** — Dark-themed Streamlit UI with tool badges that show which source answered, plus example queries to start from.

### Available Tools

| Tool | Purpose | Data Source |
|------|---------|-------------|
| **InstitutionsDBTool** | Query universities, colleges, schools, madrasas, govt. offices | SQLite — `institutions.db` |
| **HospitalsDBTool** | Query hospitals, clinics, medical facilities | SQLite — `hospitals.db` |
| **RestaurantsDBTool** | Query restaurants, cuisines, ratings, locations | SQLite — `restaurants.db` |
| **WebSearchTool** | General knowledge (policies, history, culture, demographics) | DuckDuckGo |

---

## Project Structure

```
multi-tool-ai-agent/
├── app.py                  # Streamlit chat UI (entry point)
├── agent.py                # LangChain ReAct agent & LLM setup
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── data/
│   ├── institutions.db     # SQLite DB — institutional data
│   ├── hospitals.db        # SQLite DB — hospital data
│   └── restaurants.db      # SQLite DB — restaurant data
└── tools/
    ├── db_tools.py         # InstitutionsDBTool, HospitalsDBTool, RestaurantsDBTool
    └── search_tool.py      # WebSearchTool (DuckDuckGo)
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- A free **HuggingFace API token** — [get one here](https://huggingface.co/settings/tokens)

### 1. Clone the Repository

```bash
git clone https://github.com/saminul-amin/multi-tool-ai-agent.git
cd multi-tool-ai-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual token:

```
HF_TOKEN=hf_your_actual_token_here
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## Datasets

The SQLite databases in `data/` are built from these HuggingFace datasets:

| Database | Source Dataset | Description |
|----------|---------------|-------------|
| `institutions.db` | [Institutional Information of Bangladesh](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh) | Universities, colleges, schools, madrasas, govt. offices |
| `hospitals.db` | [All Bangladeshi Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals) | Hospitals, clinics, and health facilities across Bangladesh |
| `restaurants.db` | [Bangladeshi Restaurant Data](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data) | Restaurants with ratings, cuisines, and locations |

---

## Architecture

```
User Query
    │
    ▼
┌──────────────────────────┐
│   LangChain ReAct Agent  │
│   (Qwen2.5-72B via HF)  │
└──────────┬───────────────┘
           │  Decides which tool to use
     ┌─────┼─────────┬──────────┐
     ▼     ▼         ▼          ▼
 Institutions  Hospitals  Restaurants  Web Search
   DB Tool      DB Tool     DB Tool      Tool
     │            │           │            │
     ▼            ▼           ▼            ▼
  SQLite       SQLite      SQLite     DuckDuckGo
     │            │           │            │
     └────────────┴───────────┴────────────┘
                      │
                      ▼
              Natural Language Answer
              (shown in Streamlit UI)
```

**How it works:**

1. The user asks a question through the Streamlit chat interface.
2. The **ReAct agent** (powered by Qwen2.5-72B on HuggingFace Inference API) reasons about which tool to invoke.
3. For **data queries**, the agent writes a SQL query and executes it against the appropriate SQLite database.
4. For **general knowledge queries**, the agent uses DuckDuckGo web search.
5. The agent formats the results into a natural language answer and returns it to the user.

---

## Example Queries

| Query | Routed To | What It Does |
|-------|-----------|--------------|
| "How many hospitals are in Dhaka division?" | `HospitalsDBTool` | Counts hospitals filtered by Dhaka |
| "List top colleges in Rajshahi district" | `InstitutionsDBTool` | Fetches institutions in Rajshahi |
| "Find restaurants in Chattogram with high ratings" | `RestaurantsDBTool` | Searches for top-rated restaurants |
| "What is the healthcare policy of Bangladesh?" | `WebSearchTool` | Searches the web for policy info |
| "How many government institutions are in Sylhet?" | `InstitutionsDBTool` | Counts govt. institutions in Sylhet |
| "Show medical college hospitals in Bangladesh" | `HospitalsDBTool` | Finds medical college hospitals |

---

## Configuration

| Setting | Value | Where |
|---------|-------|-------|
| LLM Model | `Qwen/Qwen2.5-72B-Instruct` | [agent.py](agent.py) |
| Temperature | `0.1` | [agent.py](agent.py) |
| Max Tokens | `1024` | [agent.py](agent.py) |
| Max Agent Iterations | `5` | [agent.py](agent.py) |
| SQL Result Limit | `50 rows` | [tools/db_tools.py](tools/db_tools.py) |

---

## Production Notes

This project runs against local SQLite copies of public datasets. Pointing the same pattern at a real business database would need a few additions:

- **Read-only access** — the agent's generated SQL is currently executed as written, so use a read-only connection or a database role that can only `SELECT`.
- **Query guardrails** — an allow-list of tables and a timeout per query.
- **Logging** — record each question, the SQL the agent wrote, and the result, so answers can be audited.

The existing limits (5 agent iterations, 50 rows per result, temperature 0.1) keep behaviour predictable but are not a security boundary.

---

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Agent framework (ReAct agent, tool abstraction) |
| `langchain-huggingface` | HuggingFace LLM integration |
| `langchain-community` | DuckDuckGo search tool |
| `streamlit` | Web-based chat UI |
| `python-dotenv` | Environment variable management |
| `duckduckgo-search` | Web search backend |

See [requirements.txt](requirements.txt) for the full list.

---

## Contact

Built by **Md. Saminul Amin**.

| Platform | Link |
|----------|------|
| Portfolio | [md-saminul-amin.vercel.app](https://md-saminul-amin.vercel.app/) |
| GitHub | [@saminul-amin](https://github.com/saminul-amin) |
| LinkedIn | [Md Saminul Amin](https://www.linkedin.com/in/md-saminul-amin/) |
| Email | [saminul.amin@gmail.com](mailto:saminul.amin@gmail.com) |

---

## License

[MIT](LICENSE)
