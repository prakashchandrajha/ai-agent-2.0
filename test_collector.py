import asyncio
from unittest.mock import patch, MagicMock
from agent.modules.collector import KnowledgeCollector, ScrapingThresholdError, dedupe_urls_by_domain
from agent.modules.pre_validator import LearningContract

print("Testing dedupe_urls_by_domain:")
urls = ['http://a.com/1', 'http://a.com/2', 'http://a.com/3', 'http://b.com/1']
deduped = dedupe_urls_by_domain(urls)
assert deduped == ['http://a.com/1', 'http://a.com/2', 'http://b.com/1'], f"Got {deduped}"
print("Dedupe OK")

async def test_3_of_3_fail():
    c = KnowledgeCollector()
    contract = LearningContract(topic="test", resolved_domain="test")
    
    with patch("agent.modules.collector.search_web", return_value=['http://a.com', 'http://b.com', 'http://c.com']), \
         patch("agent.modules.collector.collect_from_urls_parallel", return_value=[]):
        try:
            await c.collect(contract)
            print("FAILED: Should have raised ScrapingThresholdError for 3/3 fails")
        except ScrapingThresholdError:
            print("Test 3/3 fail OK")

async def test_1_of_3_succeed():
    c = KnowledgeCollector()
    contract = LearningContract(topic="test", resolved_domain="test")
    
    with patch("agent.modules.collector.search_web", return_value=['http://a.com', 'http://b.com', 'http://c.com']), \
         patch("agent.modules.collector.collect_from_urls_parallel", return_value=['content1']), \
         patch("agent.modules.collector.get_chunker", return_value=MagicMock()), \
         patch.object(c, "_extract_from_llm", return_value={}), \
         patch.object(c, "_entropy_filter", return_value=MagicMock()):
        try:
            await c.collect(contract)
            print("Test 1/3 succeed OK (no error)")
        except ScrapingThresholdError:
            print("FAILED: Raised ScrapingThresholdError for 1/3 success")

asyncio.run(test_3_of_3_fail())
asyncio.run(test_1_of_3_succeed())

