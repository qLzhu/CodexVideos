.PHONY: test cli-help

test:
	pytest -q

cli-help:
	python -m app.cli --help
