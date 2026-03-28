import asyncio
from unittest.mock import AsyncMock, patch
from agent.modules.executor import ExecutionLearner
from agent.modules.verifier import VerificationResult
from agent.knowledge.eku_schema import ExecutableKnowledgeUnit

async def test_circular_fix():
    learner = ExecutionLearner()
    
    raw = ExecutableKnowledgeUnit()
    raw.topic = "test_topic"
    raw.domain = "test_domain"
    raw.definitions = ["def1"]
    raw.invariants = ["inv1"]
    verified = VerificationResult(raw=raw, verification_passed=True)
    
    mock_tests = {
        "normal": [{"description": "test 1", "code": "print('hello')"}]
    }
    
    from agent.sandbox.runner import SandboxResult
    
    async def mock_llm_json(*args, **kwargs):
        # Call 1
        return mock_tests
        
    async def mock_llm_generate(*args, **kwargs):
        # Call 2
        assert kwargs.get('json_mode') is False, "Call 2 must not force JSON"
        return "assert True"
        
    async def mock_sandbox_run(code, lang):
        if "assert True" in code:
            return SandboxResult(passed=True, stdout="hello", stderr="", execution_time_ms=10, return_code=0)
        else:
            return SandboxResult(passed=True, stdout="hello", stderr="", execution_time_ms=5, return_code=0)

    learner.sandbox.run = AsyncMock(side_effect=mock_sandbox_run)
    
    mock_client = AsyncMock()
    mock_client.generate = mock_llm_generate
    
    with patch('agent.modules.executor.llm_complete_json', new=AsyncMock(side_effect=mock_llm_json)):
        with patch('agent.llm.client.get_llm_client', return_value=mock_client):
            results = await learner.learn_by_doing(verified)
            
    assert len(results.passed) == 1
    assert "assert True" in results.passed[0].code
    print("ALL TESTS PASSED")

asyncio.run(test_circular_fix())
