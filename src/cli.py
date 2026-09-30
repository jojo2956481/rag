from pathlib import Path
from tqdm import tqdm
from src.models import Chunk, ChunkIndex
from src.tokenize import tokenize
import bm25s


class Indexing():
    def __init__(self):
        self.max_chunk = 0

    def find_section(self, text, format: str):
        sections: list[tuple[int, int]] = []
        section_start = 0
        offset = 0
        if format == "md":
            for line in text.splitlines(keepends=True):
                if line.startswith("#") and offset > section_start:
                    sections.append((section_start, offset))
                    section_start = offset
                offset += len(line)
            if section_start < len(text):
                sections.append((section_start, len(text)))
            return sections
        else:
            lines = text.splitlines(keepends=True)
            for i, line in enumerate(lines):
                if line.startswith("async def") and offset > section_start or\
                    line.startswith("class ") and offset > section_start or\
                    line.startswith("def ") and offset > section_start and i > 0 and\
                    not lines[i - 1].lstrip().startswith("@") or\
                    line.startswith("@") and offset > section_start:
                    sections.append((section_start, offset))
                    section_start = offset
                offset += len(line)
            if section_start < len(text):
                sections.append((section_start, len(text)))
        return sections

    def open_file(self, files: str, max_chunk: int, format: str):
        self.max_chunk = max_chunk
        all_chunks: list[Chunk] = []
        for path in tqdm(files, desc="Chunking", unit="file"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                tqdm.write(f"Skipped {path}: {e}")
                continue
            sections = self.find_section(text, format)
            for sec_start, sec_end in sections:
                for start in range(sec_start, sec_end, self.max_chunk):
                    end = min(start + self.max_chunk, sec_end)
                    all_chunks.append(Chunk(
                        file_path=str(path),
                        first_character_index=start,
                        last_character_index=end,
                        text=text[start:end]
                        ))
        corpus_tokens = [tokenize(chunk.text) for chunk in tqdm(
            all_chunks, desc="Tokenizing", unit="chunk")]
        return all_chunks, corpus_tokens


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
            raise ValueError(e)
        print(
            f"Ingestion complete! Indexed {len(data.chunks)} chunks "
            f"under {index_dir}/")



    def search(self, query: str, k: int = 5) -> None:
        print(f"TODO search {query!r} k={k}")

    def search_dataset(self, dataset_path: str, save_directory: str,
                       k: int = 10) -> None:
        print("TODO search_dataset")

    def answer(self, query: str, k: int = 5) -> None:
        print("TODO answer")

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str) -> None:
        print("TODO answer_dataset")

    def evaluate(self, student_search_results_path: str,
                 dataset_path: str) -> None:
        print("TODO evaluate")
