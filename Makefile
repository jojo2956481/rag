export UV_CACHE_DIR := /goinfre/$(USER)/.cache/uv
export HF_HOME      := /goinfre/$(USER)/.cache/huggingface
export UV_LINK_MODE := copy

ARGS := --help

install:
	@uv sync --extra dev

run: install
	@uv run rag $(ARGS)

ingest : install
	@uv run rag ingest $(DIR)

query : install
	@uv run rag "$(Q)" --top_k=$(or $(K),5)

debug:
	@uv run python -m pdb -m llm_sdk.cli $(ARGS)

clean:
	@rm -rf */*/__pycache__/ */*/*/__pycache__ */*__pycache__
	@rm -rf .mypy_cache/

lint:
	@uv run flake8 src/
	@uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip

lint-strict:
	@uv run mypy src/ --strict --follow-imports=silent

.PHONY: install run debug clean lint lint-strict query ingest