VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: all venv install run clean activate

all: venv install

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) genera_archivos_de_conceptos.py

activate:
	@echo "Para activar el entorno virtual, ejecuta:"
	@echo "source $(VENV_DIR)/bin/activate"

clean:
	rm -rf $(VENV_DIR)