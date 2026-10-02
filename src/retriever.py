from src.tokenize import tokenize
from pathlib import Path
from src.models import ChunkIndex
import bm25s
from src.tokenize import tokenize


class Retriever():
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        with open(Path(index_dir) / "chunks.json", encoding="utf-8") as f:
            self.chunks = ChunkIndex.model_validate_json(f.read()).chunks
        self.bm25 = bm25s.BM25.load(str(Path(index_dir) / "bm25"))

    def search(self, queries: str, k: int):
        k = min(k, len(self.chunks))
        tokens = [tokenize(q) for q in queries]
        results, _ = self.bm25.retrieve(tokens, k=k, show_progress=False)
        all_results = []
        for row in results:
            chunks_for_question = []
            for i in row:
                chunks_for_question.append(self.chunks[int(i)])
            all_results.append(chunks_for_question)
        return all_results




        