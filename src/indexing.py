from tqdm import tqdm
from src.models import Chunk
from src.tokenize import tokenize


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
