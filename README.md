# 🇧🇩 Multi-Tool AI Agent for Bangladesh

A professional AI Agent built with **LangChain** and **FastAPI** that features a beautiful chat interface. It answers data-specific queries from three Bangladesh datasets and uses web search for general knowledge questions.

![Architecture](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)
![LLM](https://img.shields.io/badge/LLM-Qwen2.5--72B-blue?style=flat-square)
![Framework](https://img.shields.io/badge/Agent-LangChain_ReAct-orange?style=flat-square)
![Search](https://img.shields.io/badge/Search-DuckDuckGo-green?style=flat-square)

## Features

| Tool | Purpose | Data Source |
|------|---------|-------------|
| **InstitutionsDBTool** | Query universities, colleges, schools, madrasas | 34,901 institutions |
| **HospitalsDBTool** | Query hospitals, clinics, health facilities | 38,886 facilities |
| **RestaurantsDBTool** | Query restaurants, ratings, locations | 12,703 restaurants |
| **WebSearchTool** | General knowledge (policies, history, culture) | DuckDuckGo Search |