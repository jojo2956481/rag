from pathlib import Path
from src.models import ChunkIndex
from src.indexing import Indexing
import bm25s
from src.retriever import Retriever


class RagCLI:
    def __init__(self):
        pass

    def index(self, max_chunk_size: int = 2000,
              raw_dir: str = "data/raw",
              index_dir: str = "data/processed") -> None:
        idx = Indexing()
        files_py = sorted(Path(raw_dir).rglob("*.py"))
        files_md = sorted(Path(raw_dir).rglob("*.md"))
        print(
            f"number of file.md: {len(files_md)}\n"
            f"number of file.py: {len(files_py)}"
            )
        chunks_py, corpus_tokens_py = idx.open_file(
            files_py,
            max_chunk_size, "py")
        chunks_md, corpus_tokens_md = idx.open_file(
            files_md,
            max_chunk_size, "md")
        print(f"chunk.md: {len(chunks_md)}\nchunk_py: {len(chunks_py)}")
        out_dir = Path(index_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        data = ChunkIndex(chunks=chunks_py + chunks_md)
        with open(out_dir / "chunks.json", "w", encoding="utf-8") as f:
            f.write(data.model_dump_json())
        retriever = bm25s.BM25()
        try:
            retriever.index(corpus_tokens_md + corpus_tokens_py)
            retriever.save(str(Path(index_dir) / "bm25"))
        except Exception as e:
            print(e)
            return
        print(
            f"Ingestion complete! Indexed {len(data.chunks)} chunks "
            f"under {index_dir}/")

    def search(
            self, query: str, k: int = 5,
            index_dir: str = "data/processed") -> None:
        if not str(query):
            print("Error")
            return
        if k <= 0:
            print("Error")
            return
        try:
            retriever = Retriever(index_dir)
        except Exception as e:
            print(e)
            return
        result = retriever.search(str(query), k)[0]
        for c in result:
            print(
                f"{c.file_path} "
                f"[{c.first_character_index}:{c.last_character_index}]")

    def search_dataset(self, dataset_path: str, save_directory: str,
                       k: int = 5) -> None:
        if not str(dataset_path):
            print("Error")
            return
        if not str(save_directory):
            print("Error")
            return
        if k <= 0:
            print("Error")
        print("TODO search_dataset")

    def answer(self, query: str, k: int = 5) -> None:
        print("TODO answer")

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str) -> None:
        print("TODO answer_dataset")

    def evaluate(self, student_search_results_path: str,
                 dataset_path: str) -> None:
        print("TODO evaluate")
