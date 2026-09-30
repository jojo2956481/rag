from pydantic import BaseModel


class Chunk(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int
    text: str


class ChunkIndex(BaseModel):
    chunks: list[Chunk]
