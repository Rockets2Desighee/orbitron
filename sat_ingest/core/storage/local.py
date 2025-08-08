from __future__ import annotations
import os
import shutil
from .base import StorageSink

class LocalSink(StorageSink):
    def __init__(self, root: str = "./data"):
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def put(self, src_path: str, dest_key: str) -> str:
        dest = os.path.join(self.root, dest_key)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src_path, dest)
        return dest