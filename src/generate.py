from transformers import AutoModelForCausalLM, AutoTokenizer
from src.models import Chunk


class Generate():
    def __init__(
            self, max_context_tokens: int = 3000,
            model_name: str = "Qwen/Qwen3-0.6B") -> None:
        self.SYSTEM_PROMPT = (
            "You answer questions about the vLLM codebase. Use only the provided "
            "sources. If they do not contain the answer, say so. Be concise.")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.max_context_tokens = max_context_tokens
        self.systeme_prompt: str = ""

    def _build_prompt(self, query: str, chunks: list[Chunk]):
        context = "\n\n".join(
            f"[Source {n}] {c.file_path}\n{c.text}"
            for n, c in enumerate(chunks, 1))
        prompt = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user",
             "content": f"Sources:\n{context}\n\nQuestion: {query}"},
        ]
        # print(prompt)
        return str(self.tokenizer.apply_chat_template(
            prompt, tokenize=False, add_generation_prompt=True,
            enable_thinking=False))

    def answer(self, query: str, chunks: list[Chunk],
               max_new_tokens: int = 256) -> str:
        chunks = list(chunks)
        prompt = self._build_prompt(query, chunks)
        while (len(self.tokenizer(prompt)["input_ids"])
               > self.max_context_tokens and len(chunks) > 1):
            chunks.pop()
            prompt = self._build_prompt(query, chunks)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        output = self.model.generate(**inputs,
                                     max_new_tokens=max_new_tokens,
                                     do_sample=False)
        new_tokens = output[0][inputs["input_ids"].shape[1]:]
        return str(self.tokenizer.decode(new_tokens,
                                         skip_special_tokens=True)).strip()
        
