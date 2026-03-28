import os
import shutil
from pathlib import Path
from agent.utils.atomic_session import AtomicLearningSession

def test_atomic_session():
    base_dir = Path("test_memory")
    if base_dir.exists():
        shutil.rmtree(base_dir)
        
    # Test 1: Exception auto cleanup
    try:
        with AtomicLearningSession("concept1", base_dir=base_dir) as session:
            temp_dir = session.temp_dir
            assert temp_dir.exists(), "Temp dir should exist"
            # Write a file
            (temp_dir / "test.txt").write_text("hello")
            raise ValueError("Something went wrong")
    except ValueError:
        pass
    
    assert not temp_dir.exists(), "Temp dir should be cleaned up on exception"
    assert not (base_dir / "concept1").exists(), "Final dir should not exist"
    
    # Test 2: Commit moves files
    with AtomicLearningSession("concept2", base_dir=base_dir) as session:
        temp_dir = session.temp_dir
        (temp_dir / "data.json").write_text('{"ok": true}')
        session.commit()
    
    assert not temp_dir.exists(), "Temp dir should be gone after commit"
    final_dir = base_dir / "concept2"
    assert final_dir.exists(), "Final dir should exist"
    assert (final_dir / "data.json").exists(), "Data file should exist in final dir"
    
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    test_atomic_session()
