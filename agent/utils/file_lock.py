"""Cross-platform file locking and atomic JSON write utility.

Provides a context manager for locking files during read/write operations
and a helper for atomic JSON writes.
Uses fcntl on Unix-like systems and msvcrt on Windows.
"""

import os
import time
import json
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Generator

try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False


@contextmanager
def file_lock(file_path: str | Path, timeout: float = 10.0) -> Generator[None, None, None]:
    """Base context manager for cross-platform advisory file locking.
    
    Args:
        file_path: Path to the file to lock.
        timeout: Maximum time to wait for the lock in seconds.
    """
    path = str(file_path)
    lock_path = f"{path}.lock"
    start_time = time.time()
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(lock_path)), exist_ok=True)
    
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT)
    try:
        while True:
            try:
                if HAS_FCNTL:
                    # Unix-like: exclusive, non-blocking lock
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                elif HAS_MSVCRT:
                    # Windows: non-blocking lock
                    msvcrt.locking(lock_fd, msvcrt.LK_NBLCK, 1)
                else:
                    raise RuntimeError("No file locking mechanism available on this platform.")
                
                break
                
            except (IOError, OSError) as e:
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Could not acquire lock on {path} after {timeout}s: {e}")
                time.sleep(0.05)
        
        yield
        
    finally:
        try:
            if HAS_FCNTL:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            elif HAS_MSVCRT:
                try:
                    msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
                except:
                    pass
        except (IOError, OSError):
            pass
        finally:
            try:
                os.close(lock_fd)
            except (IOError, OSError):
                pass


@contextmanager
def locked_file(file_path: str | Path, mode: str = "r", timeout: float = 10.0) -> Generator[Any, None, None]:
    """Context manager that locks a file and yields the file object."""
    with file_lock(file_path, timeout):
        with open(file_path, mode) as f:
            yield f


def atomic_json_write(file_path: str | Path, data: Any, timeout: float = 10.0) -> None:
    """Safely write JSON to a file using locking and atomic replacement."""
    path = Path(file_path)
    with file_lock(path, timeout):
        dir_path = path.parent
        with tempfile.NamedTemporaryFile("w", dir=dir_path, delete=False) as tf:
            json.dump(data, tf, indent=2)
            temp_name = tf.name
        os.replace(temp_name, path)
