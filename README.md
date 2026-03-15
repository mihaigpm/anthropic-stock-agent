# Anthropic AI Gateway & Agent UI for Stock Market

A full-stack, containerized AI application demonstrating advanced LLM integration, agentic tool use (function calling), and a production-ready UI. Built as part of a product engineering sprint.

## 🚀 Key Features

* **Agentic Tool Use:** Implements a multi-turn, stateful loop using Claude 4.6. The model dynamically decides when to defer to local Python tools for real-time data.
* **Scalable Plugin Architecture:** Uses an Abstract Base Class (`BaseTool`) and a Service Locator pattern (`ToolRegistry`) to decouple tool execution from the core FastAPI routing.
* **Real-Time Data Integration:** Includes a `StockPriceTool` that fetches live market data via `yfinance` and feeds it back to the LLM for synthesis.
* **Rich UI Rendering:** A React frontend styled with Tailwind CSS, featuring full Markdown parsing, GitHub Flavored Markdown (tables), and a developer-focused dark-mode input interface.
* **Production Infrastructure:** Fully containerized using Docker and Docker Compose, ensuring environment parity and rapid deployment.

## 🛠️ Tech Stack

**Backend:**
* Python 3.11
* FastAPI & Uvicorn (Gateway API)
* Anthropic Python SDK
* yfinance (External Data)

**Frontend:**
* React (Vite)
* Tailwind CSS & `@tailwindcss/typography`
* `react-markdown` & `remark-gfm`

**Infrastructure:**
* Docker & Docker Compose

## 📂 Architecture

```text
anthropic-product-sprint/
├── docker-compose.yml       # Multi-container orchestration
├── frontend/                # React/Vite SPA
│   ├── src/
│   │   ├── App.tsx          # Main UI and chat interface
│   │   └── useClaude.ts     # API hook for agentic endpoints
│   └── tailwind.config.js
└── ai-gateway/              # FastAPI Backend
    ├── main.py              # API routes and Anthropic client setup
    ├── requirements.txt
    ├── Dockerfile           # Layer-cached container definition
    └── tools/               # Agentic Tools Module
        ├── __init__.py      # Public module API
        ├── base.py          # Abstract Base Class contract
        ├── registry.py      # Tool discovery and execution service
        └── stock_tool.py    # Concrete yfinance implementation
```

## 🚦 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.
* An Anthropic API Key.

### Installation

1. Clone the repository and navigate to the root directory.
2. Create a `.env` file inside the `ai-gateway/` directory and add your API key:
   ```env
   ANTHROPIC_API_KEY=your_api_key_here
   ```
3. Boot the infrastructure:
   ```bash
   docker compose up --build
   ```

### Usage
* **Frontend UI:** Open your browser to `http://localhost:5173`
* **Backend API:** Running on `http://localhost:8000`

Try asking Claude: *"Compare the current stock prices of AAPL and MSFT."* Watch the backend execute parallel tool calls and the frontend render the resulting data table