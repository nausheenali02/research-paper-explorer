# 🔬 Research Paper Explorer

An AI-powered research assistant that searches **arXiv papers and web sources**, analyzes research queries, summarizes relevant studies, and compares different approaches using a multi-agent workflow built with **LangGraph and Google Gemini**.

Research Paper Explorer simplifies the initial stages of literature research by turning a research question into structured summaries and comparative insights.

## ✨ Features

- **Intelligent Query Analysis:** Identifies the topic and research task from a natural-language query.
- **Automated Research Planning:** Creates a research plan and selects relevant sources.
- **Multi-Source Search:** Retrieves research papers from arXiv and relevant information from the web.
- **Paper Relevance Filtering:** Evaluates retrieved sources against the user's research query.
- **Structured Paper Summarization:** Extracts key information, including the problem, approach, datasets, results, and limitations.
- **Comparative Analysis:** Identifies similarities, differences, and promising approaches across the selected sources.
- **Interactive Web Interface:** Submit research questions and view summaries and comparisons through a custom frontend.
- **REST API:** Connects the frontend to the research workflow through FastAPI.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| LangGraph | Multi-agent workflow orchestration |
| LangChain | LLM integration and structured outputs |
| Google Gemini | Query analysis, summarization, and comparison |
| arXiv API | Academic paper retrieval |
| Tavily Search | Web search |
| FastAPI | Backend REST API |
| Pydantic | Structured data validation |
| HTML, CSS, JavaScript | Frontend interface |
| Git and GitHub | Version control |

## 🧠 How It Works

The project follows a modular, multi-agent research pipeline.

1. **Query Analyzer** — Understands the user's research question and identifies the topic and task.
2. **Research Planner** — Develops a search strategy and chooses the appropriate sources.
3. **Source Router** — Directs the workflow to the selected arXiv and web search tools.
4. **Research Retrieval** — Collects relevant papers and web sources.
5. **Paper Filter** — Evaluates source relevance to the research question.
6. **Paper Summarizer** — Generates structured summaries of the selected sources.
7. **Comparison Agent** — Synthesizes the summaries into an overall comparison, similarities, differences, and a discussion of promising approaches.

The workflow is orchestrated using LangGraph, while the FastAPI backend exposes the research pipeline to the frontend.

## 🏗️ Project Structure

```text
research-paper-explorer/
│
├── app/
│   ├── agents/
│   │   ├── query_analyzer.py
│   │   ├── research_planner.py
│   │   ├── paper_filter.py
│   │   ├── paper_summarizer.py
│   │   └── comparison_agent.py
│   │
│   ├── tools/
│   │   ├── arxiv_search.py
│   │   └── web_search.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── api.py
│   ├── main.py
│   ├── state.py
│   ├── models.py
│   └── llm.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The tree above describes the expected project layout. Keep it aligned with the files actually present in your repository.*

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.12
- Git
- A Google Gemini API key
- A Tavily API key

### 1. Clone the Repository

```bash
git clone https://github.com/nausheenali02/research-paper-explorer.git
cd research-paper-explorer
```

### 2. Create and Activate a Virtual Environment

**macOS / Linux**

```bash
python3.12 -m venv venv
source venv/bin/activate
```

If your system uses `python3` instead of `python3.12`, use the appropriate Python 3.12 executable.

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Obtain API keys from:

- Google AI Studio: https://aistudio.google.com/
- Tavily: https://tavily.com/

Replace the placeholder values with your own keys. **Never commit your `.env` file or expose API keys in your code or public repository.**

### 5. Run the Backend

From the project root, start the FastAPI server:

```bash
python -m uvicorn app.api:app --reload
```

The API will be available at:

- Base URL: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep this terminal running while using the application.

### 6. Run the Frontend

Open a **second terminal** in the project root and activate the virtual environment if necessary:

```bash
source venv/bin/activate
```

Start a local static web server:

```bash
python -m http.server 5500 --directory frontend
```

Open http://127.0.0.1:5500 in your browser.

Keep both terminals running. The frontend sends research requests to the local FastAPI backend.

## 🚀 Example Research Queries

Try questions such as:

- `Find recent papers on RAG hallucination and compare their approaches.`
- `Compare transformer-based and CNN-based approaches for image classification.`
- `Explore recent research on retrieval-augmented generation for question answering.`
- `Find research on deep learning approaches for medical image classification.`

The results include query analysis, a research plan, relevant sources, structured summaries, and a comparative analysis.

## 🔌 API Reference

### `GET /`

Checks whether the API is running.

Example response:

```json
{
  "message": "Research Paper Explorer API is running!"
}
```

### `GET /health`

Returns the API health status.

### `POST /research`

Runs the research workflow for a user query.

**Request body:**

```json
{
  "query": "Find recent papers on RAG hallucination and compare their approaches."
}
```

The response includes:

- Original research query
- Identified topic and research task
- Search plan and selected sources
- Relevant papers with metadata and source URLs
- Structured summaries
- Comparative analysis

For the full request and response schemas, start the backend and visit `/docs`.

## ⚠️ Limitations

- The quality and relevance of results depend on the availability of external sources and search services.
- Web sources and academic papers may differ in reliability and evidence quality.
- AI-generated summaries and comparisons can contain inaccuracies or omit important context.
- API access, rate limits, and network connectivity can affect execution.
- Important findings should always be verified against the original publications.

## 🔮 Future Improvements

Potential improvements include:

- More robust source metadata validation and citation handling
- Improved ranking and filtering of research sources
- Exporting research summaries and comparisons
- Deployment with production-ready configuration
- Additional academic search providers

## 🎯 Learning Outcomes

This project explores practical applications of:

- Multi-agent workflow orchestration with LangGraph
- LLM-powered research and structured generation
- Academic and web search integration
- Relevance filtering and comparative analysis
- REST API development using FastAPI
- Connecting a custom frontend to an AI backend
- Environment configuration and dependency management

## 👩‍💻 Author

**Nausheen Ali**

- GitHub: https://github.com/nausheenali02
- LinkedIn: https://www.linkedin.com/in/nausheen-ali-72583628a/

---

*Built as a hands-on exploration of multi-agent AI systems and LLM-powered research workflows.*
