import fire


class RagCLI:
    def index(self, max_chunk_size: int = 2000,
              raw_dir: str = "data/raw",
              index_dir: str = "data/processed") -> None:
        print(f"TODO index (max_chunk_size={max_chunk_size})")

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

