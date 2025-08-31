import time
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any


@asynccontextmanager
async def trace_execution_time(trace: Dict[str, Any]):
    """Context manager to trace execution time of operations"""
    start_time = time.time()
    try:
        yield
    finally:
        execution_time = time.time() - start_time
        trace["execution_time"] = execution_time