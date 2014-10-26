default: run


PACKAGE = django_authgroupex
MANAGE_PY = python manage.py


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

.PHONY: default run test dist clean resetdb
