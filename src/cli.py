from pathlib import Path
from tqdm import tqdm


class Indexing():
    def __init__(self):
        self.max_chunk = 0
        self.text: str | None = None
        self.lst_chunk: list[str] = []
        self.count_chunk: int = 0

    def open_file(self, files: str, max_chunk: int):
        self.max_chunk = max_chunk
        for path in tqdm(files, desc="Chunking", unit="file"):
            try:
                self.text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                print(e)

    def nb_chunk(self):
        for _ in range(0, len(self.text), self.max_chunk):
            self.count_chunk += 1


class RagCLI:
    def __init__(self):
        self.files_md: list[Path] = []
        self.files_py: list[Path] = []
        self.idx = Indexing()

    def index(self, max_chunk_size: int = 2000,
              raw_dir: str = "data/raw",
              index_dir: str = "data/processed") -> None:
        self.files_py = sorted(Path(raw_dir).rglob("*.py"))
        self.files_md = sorted(Path(raw_dir).rglob("*.md"))
        print(
            f"number of file.md: {len(self.files_md)}\n"
            f"number of file.py: {len(self.files_py)}"
            )
        self.idx.open_file(self.files_py, max_chunk_size)
        self.idx.nb_chunk()
        print(f" number of chunk_py: {self.idx.count_chunk}")

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

