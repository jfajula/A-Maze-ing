install: 
	pip install poetry
	poetry install

run:
	python3 a_maze_ing.py config.txt

build:
	python3 -m build
	cp ./mazegen-1.0.0-py3-none-any.whl .

debug:
	python3 -m pdb a_maze_ing.py default_config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 --exclude=.venv,mlx .
	python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'

.PHONY: install run build debug clean lint