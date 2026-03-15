import yfinance as yf
from .base import BaseTool

class StockPriceTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_stock_price"

    @property
    def definition(self) -> dict:
        return {
            "name": self.name,
            "description": "Get real-time stock price and market data for a ticker symbol.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol (e.g., AAPL, NVDA)"
                    }
                },
                "required": ["ticker"]
            }
        }

    async def execute(self, ticker: str) -> dict:
        try:
            stock = yf.Ticker(ticker)
            # Fetching fast data (non-blocking in a real production env)
            info = stock.fast_info
            return {
                "ticker": ticker.upper(),
                "current_price": round(info.last_price, 2),
                "currency": "USD",
                "market_cap": f"{info.market_cap / 1e9:.2f}B"
            }
        except Exception as e:
            return {"error": f"Could not fetch data for {ticker}: {str(e)}"}