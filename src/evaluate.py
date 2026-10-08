from src.models import MinimalSource


def iou(a: MinimalSource, b: MinimalSource) -> float:
    if a.file_path != b.file_path:
        return 0.0
    inter = max(0, min(a.last_character_index, b.last_character_index)
                - max(a.first_character_index, b.first_character_index))
    union = ((a.last_character_index - a.first_character_index)
             + (b.last_character_index - b.first_character_index) - inter)
    return inter / union if union > 0 else 0.0
