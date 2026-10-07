from pathlib import Path
from src.models import ChunkIndex, MinimalSearchResults, MinimalSource, StudentSearchResults, RagDataset
from src.indexing import Indexing
import bm25s
from src.retriever import Retriever
from tqdm import tqdm
from src.tokenize import tokenize


class RagCLI:
    def __init__(self):
        pass

    def index(self, max_chunk_size: int = 2000,
              raw_dir: str = "data/raw",
              index_dir: str = "data/processed") -> None:
        idx = Indexing()
        prefix = "data/raw/vllm-0.10.1/"
        files_py = sorted(Path(raw_dir).rglob("*.py"))
        files_md = sorted(Path(raw_dir).rglob("*.md"))
        print(
            f"number of file.md: {len(files_md)}\n"
            f"number of file.py: {len(files_py)}"
            )
        chunks_py = idx.open_file(
            files_py,
            max_chunk_size, "py")
        chunks_md = idx.open_file(
            files_md,
            max_chunk_size, "md")
        all_chunks = chunks_md + chunks_py
        print(f"chunk.md: {len(chunks_md)}\nchunk_py: {len(chunks_py)}")
        corpus_tokens = [tokenize(c.text) + tokenize(c.file_path.removeprefix(prefix)) for c in tqdm(
            all_chunks, desc="Tokenizing", unit="chunk")]
        out_dir = Path(index_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        data = ChunkIndex(chunks=all_chunks)
        with open(out_dir / "chunks.json", "w", encoding="utf-8") as f:
            f.write(data.model_dump_json())
        retriever = bm25s.BM25()
        try:
            retriever.index(corpus_tokens)
            retriever.save(str(Path(index_dir) / "bm25"))
        except Exception as e:
            print(e)
            return
        print(
            f"Ingestion complete! Indexed {len(data.chunks)} chunks "
            f"under {index_dir}/")

    def search(
            self, query: str, k: int = 10,
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
        result = retriever.search([str(query)], k)[0]
        for c in result:
            print(
                f"{c.file_path} "
                f"[{c.first_character_index}:{c.last_character_index}]")

    def search_dataset(self, dataset_path: str, save_directory: str,
                       k: int = 10, index_dir: str = "data/processed") -> None:
        if not str(dataset_path):
            print("Error")
            return
        try:
            with open(dataset_path, encoding="utf-8") as f:
                dataset = RagDataset.model_validate_json(f.read())
        except OSError as e:
            print(e)
            return
        if not str(save_directory):
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
        questions = dataset.rag_questions
        all_chunks = retriever.search([q.question for q in questions], k)
        results: list[MinimalSearchResults] = []
        for q, chunks in tqdm(zip(questions, all_chunks),
                              total=len(questions), desc="Searching",
                              unit="question"):
            sources = [MinimalSource(
                file_path=c.file_path,
                first_character_index=c.first_character_index,
                last_character_index=c.last_character_index,
            ) for c in chunks]
            results.append(MinimalSearchResults(
                question_id=q.question_id, question=q.question,
                retrieved_sources=sources))

        output = StudentSearchResults(search_results=results, k=k)
        out_path = Path(save_directory) / Path(dataset_path).name
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(output.model_dump_json(indent=2))
        except OSError as e:
            print(f"Error: cannot write {out_path}: {e}")
            return
        print(f"Saved student_search_results to {out_path}")

    def answer(self, query: str, k: int = 5) -> None:
        print("TODO answer")

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str) -> None:
        print("TODO answer_dataset")

    def evaluate(self, student_search_results_path: str,
                 dataset_path: str) -> None:
        try:
            with open(student_search_results_path, encoding="utf-8") as f:
                search_results = StudentSearchResults.model_validate_json(f.read())
        except OSError as e:
            print(e)
            return
        try:
            with open(dataset_path, encoding="utf-8") as f:
                dataset = RagDataset.model_validate_json(f.read())
        except OSError as e:
            print(e)
            return
        
        
        print("TODO evaluate")
