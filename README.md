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