VENV?=venv
PYTHON?=$(VENV)/bin/python3
PIP?=$(PYTHON) -m pip

venv:$(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

run:
	$(PYTHON) src/main.py

clean:
	@rm -rf $(VENV)