"""DuckDuckGo HTML search scraper using Scrapling."""

import logging
from urllib.parse import unquote

from scrapling.fetchers import Fetcher

from agent.config import get_settings

logger = logging.getLogger(__name__)


def search_web(topic: str, max_results: int | None = None) -> list[str]:
    """
    Search DuckDuckGo HTML for a topic and return organic result URLs.
    
    Args:
        topic: The search query
        max_results: Max number of URLs to return. Defaults to MAX_SOURCES from config.
        
    Returns:
        List of URL strings.
    """
    settings = get_settings()
    limit = max_results or settings.max_sources
    
    query = "+".join(topic.split())
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    
    logger.info(f"🔍 Searching web for: {topic}")
    
    try:
        # Use Scrapling to bypass basic blocks
        page = Fetcher.get(search_url, stealthy_headers=True, timeout=15)
        
        urls = []
        # DuckDuckGo HTML organic results are usually inside .result__url
        result_links = page.css('.result__url')
        
        for link in result_links:
            href = link.attrib.get('href', '')
            if not href:
                continue
                
            # Clean up DDG redirect format if present (e.g. //duckduckgo.com/l/?uddg=https...)
            if "uddg=" in href:
                try:
                    actual_url = unquote(href.split("uddg=")[1].split("&")[0])
                    urls.append(actual_url)
                except IndexError:
                    pass
            elif href.startswith("http"):
                urls.append(href)
                
            if len(urls) >= limit:
                break
                
        logger.info(f"✅ Found {len(urls)} URLs")
        return urls
        
    except Exception as e:
        logger.error(f"❌ Web search failed: {e}")
        return []
