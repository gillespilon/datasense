check:
	@flake8 --select=F datasense

lint:
	@flake8 datasense

test:
	@pytest -vv

coverage:
	@coverage html

# Hehe
.PHONY: test coverage
