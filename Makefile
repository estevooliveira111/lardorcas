VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: help install venv run test clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv     - Cria o ambiente virtual"
	@echo "  make install  - Instala as dependências do projeto"
	@echo "  make run      - Executa o servidor Flask"
	@echo "  make run-dev      - Executa o servidor Flask em modo desenvolvimento"
	@echo "  make test     - Roda os testes do projeto"
	@echo "  make clean    - Remove arquivos desnecessários"

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	FLASK_APP=app.py FLASK_ENV=production $(PYTHON) -m flask run

run-dev: install
	FLASK_APP=app.py FLASK_ENV=development $(PYTHON) -m flask run --debug

test: install
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete