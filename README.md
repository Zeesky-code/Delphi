# Delphi

Delphi is a powerful, multi-agent financial research system built with FastAPI and the Mistral AI SDK. It automates the process of gathering, analyzing, and summarizing financial data to generate insightful reports from a single user query.

## Features

* **Multi-Agent System:** Utilizes a specialized **Researcher Agent** for data gathering and an **Analyst Agent** for data synthesis and reporting.
* **AI-Powered Tool Use:** The Researcher Agent dynamically chooses which tools to use (e.g., fetching news, getting financial data) based on the user's query, powered by Mistral's function-calling capabilities.
* **Live Data Integration:** Fetches up-to-date news from **NewsAPI** and core company financial data from **Alpha Vantage**.
* **Asynchronous Backend:** Built on **FastAPI** for high performance and concurrent processing of I/O-bound tasks.
* **Performance Caching:** Implements an in-memory TTL cache with `cachetools` to reduce redundant API calls, lower costs, and improve response times.
* **Automatic API Docs:** Uses  FastAPI and Pydantic to provide interactive API documentation via Swagger UI.

---

## Tech Stack

* **Backend:** FastAPI, Uvicorn
* **AI:** Mistral AI Python SDK (`mistralai`)
* **HTTP Client:** HTTPX
* **Caching:** cachetools
* **Configuration:** python-dotenv

---

## Project Architecture

Delphi operates using a simple yet powerful two-agent pipeline.


1.  **User Request**: The user submits a stock ticker and a high-level research query.
2.  **Researcher Agent**: This agent receives the query. It uses the Mistral LLM to decide which data-gathering tools are necessary. It then executes these tools in parallel to fetch live news and financial data.
3.  **Analyst Agent**: The raw, structured data from the Researcher is passed to this agent. It uses a separate LLM prompt to analyze the combined data and generate a well-structured, human-readable report in Markdown format.
4.  **Final Report**: The final report is logged, representing the completed task.

---

## Setup and Installation

Follow these steps to get Delphi running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Zeesky-code/Delphi.git
cd delphi
```

### 2. Create and Activate a Virtual Environment

* **macOS / Linux**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **Windows**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

You'll need API keys for the services Delphi uses. Create a file named `.env` in the root of the project directory.

```bash
touch .env
```

Copy and paste the following into the `.env` file, replacing the placeholder text with your actual API keys.

```ini
# .env

MISTRAL_API_KEY="your_mistral_api_key_here"
NEWS_API_KEY="your_news_api_key_here"
ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key_here"
```

---

## How to Run

### 1. Start the Server

With your virtual environment active, run the following command from the root `delphi/` directory:

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables hot-reloading, so the server will automatically restart when you make code changes.

### 2. Access the API

The API will be running at `http://127.0.0.1:8000`.

For interactive testing and documentation, open your browser and navigate to:

**`http://127.0.0.1:8000/docs`**

### 3. Making a Request

You can use the interactive docs or a tool like `cURL` to make a request to the `/research/` endpoint.

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/research/](http://127.0.0.1:8000/research/)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ticker": "TSLA",
  "query": "Analyze Tesla’s recent performance and position in the EV market."
}'
```

The server will immediately respond with a `task_id` and begin the agent workflow in the background. You can monitor the progress in the terminal where `uvicorn` is running.