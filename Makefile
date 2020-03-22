check:
	@flake8 --select=F datasense
	@safety check
	@bandit datasense

lint:
	@flake8 datasense
	@mypy --strict datasense
	@safety check
	@bandit datasense

test:
	@pytest -vv

coverage:
	@coverage html

# Hehe
.PHONY: test coverage
