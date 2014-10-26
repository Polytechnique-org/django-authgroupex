default: run

PACKAGE = django_authgroupex
MANAGE_PY = python manage.py

# Use current python binary instead of system default.
COVERAGE = python $(shell which coverage)

run:
	$(MANAGE_PY) runserver

test:
	$(MANAGE_PY) test $(PACKAGE)

dist:
	python setup.py sdist

clean:
	find . -name '*.pyc' -delete
	rm -rf build dist $(PACKAGE).egg-info

resetdb:
	rm -f django_authgroupex_dev/db.sqlite3
	$(MANAGE_PY) migrate --noinput

coverage:
	$(COVERAGE) erase
	$(COVERAGE) run "--include=$(PACKAGE)/*.py" --branch setup.py test
	$(COVERAGE) report "--include=$(PACKAGE)/*.py"
	$(COVERAGE) html "--include=$(PACKAGE)/*.py"

.PHONY: default run test dist clean resetdb coverage
