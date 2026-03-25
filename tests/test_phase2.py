import asyncio
import logging

from agent.services.embedder import get_embedder
from agent.services.web_scraper import scrape_page
from agent.services.web_search import search_web

logging.basicConfig(level=logging.INFO)


async def test_embedder():
    print("Testing Embedder...")
    embedder = get_embedder()
    
    sentences = [
        "A decorator is a design pattern that allows behavior to be added.",
        "Decorators in Python dynamically alter the functionality of a function.",
        "I love eating pizza on Fridays.",
    ]
    
    # These two should be semantically similar > 0.8
    # The third is completely different
    
    import numpy as np
    vectors = embedder.embed_texts(sentences)
    vectors = np.array(vectors)
    similarity = np.dot(vectors, vectors.T)
    
    print(f"Similarity 0-1: {similarity[0, 1]:.3f}")
    print(f"Similarity 0-2: {similarity[0, 2]:.3f}")
    
    assert similarity[0, 1] > 0.6, "Sentences 0 and 1 should be similar"
    assert similarity[0, 2] < 0.4, "Sentences 0 and 2 should NOT be similar"
    
    print("✅ Embedder test passed\n")


async def test_search_and_scraper():
    print("Testing Scrapling DuckDuckGo Search...")
    urls = search_web("python decorators example", max_results=2)
    print(f"Found URLs: {urls}")
    assert len(urls) > 0, "Should find at least 1 URL"
    
    print(f"\nTesting Scrapling on {urls[0]}")
    content = scrape_page(urls[0])
    
    print(f"Extracted {len(content)} chars.")
    print("Sample content:")
    print(content[:500])
    assert len(content) > 100, "Should extract meaningful content"
    
    print("\n✅ Scraper test passed")


async def main():
    await test_embedder()
    await test_search_and_scraper()

if __name__ == "__main__":
    asyncio.run(main())
