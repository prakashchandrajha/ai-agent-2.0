import asyncio
import logging
from agent.knowledge.eku_schema import ExecutableKnowledgeUnit
from agent.knowledge.eku_store import get_eku_store
from agent.services.chunker import get_chunker

logging.basicConfig(level=logging.INFO)

async def test_chunker():
    print("--- Testing Semantic Chunker ---")
    chunker = get_chunker()
    text = "Word " * 500  # 500 words, roughly 600 tokens
    
    # Force a small chunk size for testing
    chunker.chunk_size = 100
    chunker.chunk_overlap = 10
    
    chunks = chunker.chunk_text(text)
    print(f"Generated {len(chunks)} chunks.")
    assert len(chunks) > 1, "Text should have been chunked."
    print("✅ Chunker works.")

async def test_dag_rollback():
    print("\n--- Testing DAG Rollback ---")
    # Reset singleton to avoid stale state from other tests
    import agent.knowledge.eku_store as eku_mod
    eku_mod._eku_store = None
    store = get_eku_store()
    
    # Clean up previous
    for f in store._store_path.glob("*.json"):
        if f.name != "index.json":
            f.unlink()
    store._index.clear()
    store._save_index()
        
    # A is foundation. B depends on A. C depends on B.
    eku_a = ExecutableKnowledgeUnit(concept="Concept A", topic="A")
    eku_b = ExecutableKnowledgeUnit(concept="Concept B", topic="B", dependencies=[eku_a.id])
    eku_c = ExecutableKnowledgeUnit(concept="Concept C", topic="C", dependencies=[eku_b.id])
    
    # Store them
    for e in [eku_a, eku_b, eku_c]:
        e.verification_status = "proven"
        store._save_eku(e)
        
    print(f"Stored {len(store._index)} EKUs.")
    assert len(store._index) == 3
    
    # Rolling back A should cascade DOWNSTREAM: B depends on A, C depends on B → all gone
    print(f"Rolling back A ({eku_a.id})...")
    store.rollback_eku(eku_a.id)
    
    print(f"Remaining in store: {len(store._index)}")
    assert len(store._index) == 0, "All dependent EKUs should be rolled back."
    print("✅ DAG Rollback cascaded successfully.")

async def main():
    await test_chunker()
    await test_dag_rollback()

if __name__ == "__main__":
    asyncio.run(main())
