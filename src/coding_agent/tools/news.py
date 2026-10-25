from datetime import date

from ..config.settings import get_config
from ..schemas.financial import NewsItem, NewsResult


class NewsClient:
    """News API client returning summaries only."""

    def __init__(self):
        self.config = get_config().news

    async def search_news(
        self,
        tickers: list[str],
        start: date,
        end: date,
        max_items: int | None = None,
    ) -> NewsResult:
        max_items = max_items or self.config.max_items
        items: list[NewsItem] = []
        return NewsResult(
            tickers=tickers,
            start=start,
            end=end,
            items=items,
            truncated=True,
        )
