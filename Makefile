default: runserver


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
	rm -rf dist $(PACKAGE).egg-info
