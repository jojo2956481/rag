from transformers import AutoModelForCausalLM, AutoTokenizer


class Generate():
    def __init__(
            self, max_context_tokens: int,
            model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.max_context_tokens = max_context_tokens
        self.systeme_prompt: str = ""

    def _build_prompt(self):
        pass

    def generate(self):
        pass
