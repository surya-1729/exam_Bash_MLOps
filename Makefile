.PHONY: bash tests all

bash:
	@bash scripts/collect.sh
	@bash scripts/preprocessed.sh
	@bash scripts/train.sh

tests:

	@uv run pytest tests/test_collect.py && \
	uv run pytest tests/test_preprocessed.py && \
	uv run pytest tests/test_model.py

all: bash tests