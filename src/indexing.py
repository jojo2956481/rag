from pathlib import Path


class Indexing():
    def __init__(self, raw_dir):
        self.files
        self.raw_dir = raw_dir

    def open_vllm(self):
        self.files = sorted(Path(self.raw_dir).rglob("*.py")) + sorted(Path(self.raw_dir).rglob("*.md"))
        print(self.files)

