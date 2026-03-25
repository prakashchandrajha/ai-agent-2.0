"""Web page fetcher and text extractor using Scrapling."""

import logging
import re

from scrapling.fetchers import Fetcher

logger = logging.getLogger(__name__)


def scrape_page(url: str) -> str:
    """
    Fetch a page and extract clean reading text using Scrapling.
    
    Args:
        url: The URL to fetch.
        
    Returns:
        Cleaned text content of the page.
    """
    logger.info(f"🌐 Fetching: {url}")
    
    try:
        page = Fetcher.get(url, stealthy_headers=True, timeout=20)
        
        # Remove script and style tags completely
        for junk in page.css("script, style, noscript, iframe, header, footer, nav, aside"):
            if hasattr(junk, "drop"):
                junk.drop()
                
        # Extract meaningful text nodes
        # We target common semantic tags for articles/documentation
        meaningful_nodes = page.css("article, main, .content, #content, p, h1, h2, h3, h4, h5, h6, li")
        
        if not meaningful_nodes:
            # Fallback to body text if semantic tags are missing
            meaningful_nodes = page.css("body")
            
        text_blocks = []
        for node in meaningful_nodes:
            # Get all text from this node and its children
            raw_text = node.xpath(".//text()").getall()
            text = " ".join(t.strip() for t in raw_text if t.strip())
            if text and text not in text_blocks:
                text_blocks.append(text)
                
        # Join and clean up whitespace
        full_text = "\n\n".join(text_blocks)
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)
        
        # Truncate if insanely large to save LLM tokens (e.g., max 20,000 chars)
        max_chars = 20000
        if len(full_text) > max_chars:
            logger.warning(f"  ⚠️ Truncating content from {len(full_text)} to {max_chars} chars")
            full_text = full_text[:max_chars] + "...\n[Content Truncated]"
            
        logger.info(f"  📄 Extracted {len(full_text)} chars of clean text")
        return full_text
        
    except Exception as e:
        logger.error(f"❌ Scraping failed for {url}: {e}")
        return ""
