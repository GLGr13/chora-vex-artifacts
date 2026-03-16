.PHONY: install run test fmt

install:
	python -m pip install -r requirements.txt

run:
	uvicorn chora.api.app:app --reload

test:
	pytest -q
